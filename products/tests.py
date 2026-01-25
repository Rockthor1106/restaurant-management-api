from decimal import Decimal

from rest_framework import status

from django.urls import reverse

from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from .models import Product

User = get_user_model()

class ProductTest(APITestCase):

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

        product1= Product.objects.create(
            name='chuleta de cerdo',
            price=Decimal('10.000'),
            is_active=True
        )

        product2= Product.objects.create(
            name='coca cola 500 Ml',
            price=Decimal('7.000'),
            is_active=False
        )

        self.products = [
            product1, 
            product2
        ]

    def test_create_product_by_admin_returns_201(self):

        self.client.force_authenticate(self.admin_user)

        product = {
            'name':'coca cola 350 Ml',
            'price':Decimal('2.500')
        }
    
        response = self.client.post(reverse('products-list'), product)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_by_non_admin_returns_403(self):

        self.client.force_authenticate(self.user)

        product = {
            'name':'coca cola 350 Ml',
            'price':Decimal('2.500')
        }
    
        response = self.client.post(reverse('products-list'), product)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_products_by_authenticated_user_returns_200(self): 

        self.client.force_authenticate(self.user)
    
        response = self.client.get(reverse('products-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products_by_unauthenticated_user_returns_403(self): 
        
        response = self.client.get(reverse('products-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_by_admin_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500')
        )

        product_update = {
            'name':'coca cola 350 Ml',
            'price':Decimal('3.500')
        }

        response = self.client.patch(reverse('products-detail', kwargs={'pk': product.pk}), product_update)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product.refresh_from_db()

        self.assertEqual(product.price, Decimal('3.500'))

    def test_update_product_by_non_admin_returns_403(self):

        self.client.force_authenticate(self.user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500')
        )

        product_update = {
            'name':'coca cola 350 Ml',
            'price':Decimal('3.500')
        }

        response = self.client.patch(reverse('products-detail', kwargs={'pk': product.pk}), product_update)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activate_product_by_admin_returns_200(self):

        self.client.force_authenticate(self.admin_user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500'),
            is_active=False
        )

        response = self.client.post(reverse('products-activate', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product.refresh_from_db()

        self.assertTrue(product.is_active)


    def test_activate_product_by_non_admin_returns_403(self):

        self.client.force_authenticate(self.user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500'),
            is_active=False
        )

        response = self.client.post(reverse('products-activate', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activate_already_active_product_returns_400(self):
        
        self.client.force_authenticate(self.admin_user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500'),
            is_active=True
        )

        response = self.client.post(reverse('products-activate', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Product is already activated')

    def test_deactivate_product_by_admin_returns_200(self): 

        self.client.force_authenticate(self.admin_user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500'),
            is_active=True
        )

        response = self.client.post(reverse('products-deactivate', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product.refresh_from_db()

        self.assertFalse(product.is_active)

    def test_deactivate_product_by_non_admin_returns_403(self):

        self.client.force_authenticate(self.user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500'),
            is_active=True
        )

        response = self.client.post(reverse('products-deactivate', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deactivate_already_deactivated_product_returns_400(self):

        self.client.force_authenticate(self.admin_user)

        product = Product.objects.create(
            name='coca cola 350 Ml',
            price=Decimal('2.500'),
            is_active=False
        )

        response = self.client.post(reverse('products-deactivate', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Product is already deactivated')

    def test_created_by_is_assigned_automatically(self):

        self.client.force_authenticate(self.admin_user)

        product = {
            'name':'coca cola 350 Ml',
            'price':Decimal('2.500')
        }
    
        response = self.client.post(reverse('products-list'), product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        retrieved_product = Product.objects.get(name='coca cola 350 Ml')
        self.assertEqual(retrieved_product.created_by, self.admin_user)

    def test_create_product_with_negative_price_returns_400(self): 

        self.client.force_authenticate(self.admin_user)

        product = {
            'name':'coca cola 350 Ml',
            'price':Decimal('-2.500')
        }
    
        response = self.client.post(reverse('products-list'), product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_active_products_endpoint_returns_only_active_products(self):

        self.client.force_authenticate(self.user)
    
        response = self.client.get(reverse('products-active'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['is_active'])
        self.assertEqual(response.data[0]['name'], 'chuleta de cerdo')
        names = [p['name'] for p in response.data]
        self.assertNotIn('coca cola 500 Ml', names)
