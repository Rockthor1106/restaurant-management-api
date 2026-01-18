from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.test import APITestCase

User = get_user_model()

class AccountsTest(APITestCase):

    def setUp(self):

        self.admin_user = User.objects.create_user(
            email='testadmin@email.com',
            username='testadminuser',
            password='testadminpassword',
            is_staff=True,
            is_superuser=True
        )

    #Por debajo DRF pasa la request pero como AnonymousUser entonces como ese usuario no tiene los permisos retorna 403 y no 401
    def test_create_user_whitout_token_403(self):

        user = {
            'email': 'test@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post('/accounts/users/', user)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_with_token_but_no_admin_403(self):

        user = {
            'email': 'test@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(
            '/accounts/users/',
            user,
            format='json',
            headers={'Authorization': 'Bearer faketoken1234567890'}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_by_admin_201(self):
        
        self.client.force_authenticate(self.admin_user)

        user = {
            'email': 'test@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post('/accounts/users/',user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users_whitout_token_403(self):

        response = self.client.get('/accounts/users/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_with_token_no_admin_403(self):

        response = self.client.get(
            '/accounts/users/',
            format='json',
            headers={'Authorization': 'Bearer faketoken1234567890'}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_by_admin_200(self):

        self.client.force_authenticate(self.admin_user)

        response = self.client.get('/accounts/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_is_not_returned_in_response_when_list(self):

        self.client.force_authenticate(self.admin_user)

        response = self.client.get('/accounts/users/')
        self.assertNotIn('password', response.data[0])

    def test_password_is_not_returned_in_response_when_create(self):
        
        self.client.force_authenticate(self.admin_user)

        user = {
            'email': 'test@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post('/accounts/users/',user)

        self.assertNotIn('password', response.data) 
    
    def test_create_user_with_invalid_username(self):

        self.client.force_authenticate(self.admin_user)

        user = {
            'email': 'admin@email.com',
            'username': 'admin',
            'password': 'testpassword'
        }

        response = self.client.post('/accounts/users/',user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], 'Username not available')
        
    def test_validate_password_is_saved_with_hash(self):

        self.client.force_authenticate(self.admin_user)

        user = {
            'email': 'test@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        self.client.post('/accounts/users/',user)
        saved_user = User.objects.get(email='test@email.com')
        self.assertNotEqual('testpassword', saved_user.password)

    def test_json_response_only_contains_expected_data(self):

        self.client.force_authenticate(self.admin_user)

        response = self.client.get('/accounts/users/')

        expected_data_keys = {'email', 'username'}
        self.assertEqual(response.data[0].keys(), expected_data_keys)

class AccountsJWTIntegrationTest(APITestCase):

    def setUp(self):

        self.admin_user = User.objects.create_user(
            email='testadmin@email.com',
            username='testadminuser',
            password='testadminpassword',
            is_staff=True,
            is_superuser=True
        )

    def test_create_user_with_real_jwt_201(self):

        token_response = self.client.post(
            '/api/token/',
            {
                'email':'testadmin@email.com',
                'password':'testadminpassword',
            },
            format='json'
        )

        user_to_create = {
            'email': 'test@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_response.data)

        response = self.client.post(
            '/accounts/users/',
            user_to_create,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {token_response.data['access']}'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertTrue(
            User.objects.filter(email='testadmin@email.com')
        )
