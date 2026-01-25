from rest_framework import status

from django.urls import reverse

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from orders.models import Order

from .models import Table


User = get_user_model()

class TableTest(APITestCase):

    def setUp(self):

        self.admin_user = User.objects.create_user(
            email='testadmin@email.com',
            username='testadminuser',
            password='testadminpassword',
            is_staff=True,
            is_superuser=True
        )

        self.user = User.objects.create_user(
            email='testuser@email.com',
            username='testuser',
            password='testuserpassword',
        )

        table1 = Table.objects.create(
            number=10,
            capacity=2,
            is_active=True
        )

        table2 = Table.objects.create(
            number=11,
            capacity=4,
            is_active=True
        )

        order = Order.objects.create(
            table=table1,
            created_by=self.admin_user
        )
        
        self.tables = [
            table1,
            table2
        ]


    def test_list_tables_by_unauthenticated_user_returns_403(self):

        response = self.client.get(reverse('tables-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_available_tables_by_unauthenticated_user_returns_403(self):
        
        response = self.client.get(reverse('tables-available'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_list_tables_by_authenticated_user_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        response = self.client.get(reverse('tables-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_available_tables_by_authenticated_user_returns_200(self):

        self.client.force_authenticate(self.user)

        response = self.client.get(reverse('tables-available'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_table_by_no_admin_user_returns_403(self):

        self.client.force_authenticate(self.user)

        table = {
            'number': 1,
            'capacity': 4
        }

        response = self.client.post(reverse('tables-list'), table)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_table_by_admin_user_returns_201(self):

        self.client.force_authenticate(self.admin_user)

        table = {
            'number': 1,
            'capacity': 4
        }

        response = self.client.post(reverse('tables-list'), table)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activate_table_by_admin_user_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=False
        )

        response = self.client.post(reverse('tables-activate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate_table_by_no_admin_user_returns_403(self):

        self.client.force_authenticate(self.user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=True
        )

        response = self.client.post(reverse('tables-deactivate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deactivate_table_by_admin_user_returns_403(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=True
        )

        response = self.client.post(reverse('tables-deactivate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate_table_with_an_active_order(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=True
        )

        order = Order.objects.create(
            table=table,
            created_by=self.admin_user
        )

        response = self.client.post(reverse('tables-deactivate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deactivate_table_already_deactivated(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=False
        )

        response = self.client.post(reverse('tables-deactivate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_table_already_activated(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=True
        )

        response = self.client.post(reverse('tables-activate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_table_by_no_admin_user_returns_403(self):

        self.client.force_authenticate(self.user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=False
        )

        response = self.client.post(reverse('tables-activate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activate_table_happy_path_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=False
        )

        response = self.client.post(reverse('tables-activate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_available_tables_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        response = self.client.get(reverse('tables-available'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['number'], 11)
        self.assertTrue(response.data[0]['is_active'])
    
    def test_table_has_active_order_returns_true(self):

        self.assertTrue(self.tables[0].has_active_order)
        self.assertFalse(self.tables[1].has_active_order)

    def test_update_table_by_non_admin_returns_403(self):

        self.client.force_authenticate(self.user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=False
        )

        table_dict = {
            'number': 1,
            'capacity': 10

        }

        response = self.client.patch(reverse('tables-detail', kwargs={'pk': table.pk}), table_dict)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modified_by_after_activate_a_table_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        table = Table.objects.create(
            number=1,
            capacity=2,
            is_active=False
        )

        response = self.client.post(reverse('tables-activate', kwargs={'pk': table.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        table.refresh_from_db()

        self.assertEqual(table.modified_by, self.admin_user)