from decimal import Decimal

from rest_framework import status

from django.urls import reverse

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from products.models import Product

from orders.models import Order, OrderStatus

from tables.models import Table

from .models import OrderItem

from .services import create_order_item

User = get_user_model()


class OrderItemTest(APITestCase):

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

        table_1 = Table.objects.create(number=1, capacity=4)
        table_2 = Table.objects.create(number=2, capacity=6)

        order_1 = Order.objects.create(
            table=table_1,
            created_by=self.admin_user
        )

        order_2 = Order.objects.create(
            table=table_2,
            created_by=self.admin_user,
            status=OrderStatus.PAID
        )

        self.orders = [
            order_1,
            order_2
        ]

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

    def test_create_item_for_active_order(self):

        self.client.force_authenticate(self.user)

        order_item = {
            'order': self.orders[0].pk,
            'product': self.products[0].pk,
            'quantity': 4
        }

        response = self.client.post(reverse('items-list'), order_item)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_item_for_inactive_order(self):

        self.client.force_authenticate(self.user)

        order_item = {
            'order': self.orders[1].pk,
            'product': self.products[0].pk,
            'quantity': 4
        }

        response = self.client.post(reverse('items-list'), order_item)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_for_inactive_product(self):

        self.client.force_authenticate(self.user)

        order_item = {
            'order': self.orders[0].pk,
            'product': self.products[1].pk,
            'quantity': 4
        }

        response = self.client.post(reverse('items-list'), order_item)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_quantity_in_active_order(self):

        self.client.force_authenticate(self.admin_user)

        order_item = create_order_item(
            order=self.orders[0],
            product=self.products[0],
            quantity=4,
        )   

        updated_order_item = {
            'quantity': 2
        }

        response = self.client.patch(reverse(
            'items-detail', kwargs={'pk': order_item.pk}
            ), updated_order_item
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_item.refresh_from_db()

        self.assertEqual(order_item.quantity, 2)

    def test_modify_quantity_in_inactive_order(self):

        self.client.force_authenticate(self.admin_user)

        order_item = create_order_item(
            order=self.orders[0],
            product=self.products[0],
            quantity=4,
        )   

        updated_order_item = {
            'quantity': 2
        }

        self.orders[0].status=OrderStatus.PAID
        self.orders[0].save()

        response = self.client.patch(reverse(
            'items-detail', kwargs={'pk': order_item.pk}
            ), updated_order_item
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_item_in_active_order(self):

        self.client.force_authenticate(self.admin_user)

        order_item = create_order_item(
            order=self.orders[0],
            product=self.products[0],
            quantity=4,
        ) 

        response = self.client.delete(
            reverse(
                'items-detail', kwargs={'pk': order_item.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_item_in_inactive_order(self):

        self.client.force_authenticate(self.admin_user)

        order_item = create_order_item(
            order=self.orders[0],
            product=self.products[0],
            quantity=4,
        ) 

        self.orders[0].status=OrderStatus.PAID
        self.orders[0].save()


        response = self.client.delete(
            reverse(
                'items-detail', kwargs={'pk': order_item.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_unit_price_is_not_modified(self):

        self.client.force_authenticate(self.admin_user)

        order_item = create_order_item(
            order=self.orders[0],
            product=self.products[0],
            quantity=4,
        )   

        updated_order_item = {
            'quantity': 2
        }

        response = self.client.patch(reverse(
            'items-detail', kwargs={'pk': order_item.pk}
            ), updated_order_item
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_item.refresh_from_db()

        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.unit_price, Decimal('10.000'))