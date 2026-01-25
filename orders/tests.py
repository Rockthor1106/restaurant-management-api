from rest_framework import status

from django.contrib.auth import get_user_model

from django.urls import reverse

from rest_framework.test import APITestCase

from tables.models import Table

from .models import Order, OrderStatus

User = get_user_model()


class OrdersTest(APITestCase):

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
        table_2 = Table.objects.create(number=1, capacity=4, is_active=False)

        self.tables = [
            table_1,
            table_2
        ]

    def test_create_order_by_authenticated_user_returns_201(self):
        
        self.client.force_authenticate(self.admin_user)

        order = {
            'table': self.tables[0].pk
        }
        
        response = self.client.post(reverse('orders-list'), order)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_by_unauthenticated_user_returns_403(self):
        
        order = {
            'table': self.tables[0].pk
        }
        
        response = self.client.post(reverse('orders-list'), order)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_by_admin_user_returns_204(self):

        self.client.force_authenticate(self.admin_user)

        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user
        )
        
        response = self.client.delete(reverse('orders-detail', kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_by_no_admin_user_returns_403(self):

        self.client.force_authenticate(self.user)

        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user
        )
        
        response = self.client.delete(reverse('orders-detail', kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_for_an_inactive_table_returns_400(self):

        self.client.force_authenticate(self.admin_user)

        order = {
            'table': self.tables[1].pk,
        }
        
        response = self.client.post(reverse('orders-list'), order)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_for_a_table_with_active_order_returns_400(self):

        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user
        )

        order = {
            'table': self.tables[0].pk,
        }

        response = self.client.post(reverse('orders-list'), order)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_for_a_table_without_active_order_returns_201(self):
        self.client.force_authenticate(self.admin_user)

        order = {
            'table': self.tables[0].pk,
        }

        response = self.client.post(reverse('orders-list'), order)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pay_order_from_a_valid_status_returns_200(self):
        
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status = OrderStatus.DELIVERED
        )

        response = self.client.post(reverse('orders-pay',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.PAID)

    def test_pay_order_from_an_invalid_status_returns_400(self):
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
        )

        response = self.client.post(reverse('orders-pay',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_order_from_a_valid_status_returns_200(self):
        
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status=OrderStatus.CREATED
        )

        response = self.client.post(reverse('orders-cancel',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.CANCELLED)


    def test_cancel_order_from_an_invalid_status_returns_400(self):
        
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status=OrderStatus.READY
        )

        response = self.client.post(reverse('orders-cancel',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_prepare_order_by_authenticated_user_returns_200(self):

        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
        )

        response = self.client.post(reverse('orders-prepare',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.IN_PREPARATION)

    def test_deliver_order_by_authenticated_user_returns_200(self):

        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status=OrderStatus.READY
        )

        response = self.client.post(reverse('orders-deliver',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.DELIVERED)

    def test_order_lifecycle_full_happy_path(self):
        
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
        )

        self.client.post(reverse('orders-prepare',  kwargs={'pk': order.pk}))
        self.client.post(reverse('orders-ready',  kwargs={'pk': order.pk}))
        self.client.post(reverse('orders-deliver',  kwargs={'pk': order.pk}))
        response = self.client.post(reverse('orders-pay',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()

        self.assertEqual(order.status, OrderStatus.PAID)

    def test_cannot_pay_order_twice_returns_400(self):
                
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status=OrderStatus.PAID
        )

        response = self.client.post(reverse('orders-pay',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_cancel_paid_order_returns_400(self):

        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status=OrderStatus.PAID
        )

        response = self.client.post(reverse('orders-cancel',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_is_not_active_after_payment(self):
        
        self.client.force_authenticate(self.admin_user)
        
        order = Order.objects.create(
            table=self.tables[0],
            created_by=self.admin_user,
            status=OrderStatus.DELIVERED
        )

        response = self.client.post(reverse('orders-pay',  kwargs={'pk': order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()

        self.assertFalse(order.is_active)
        

    

    
        
