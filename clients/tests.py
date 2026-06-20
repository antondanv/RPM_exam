from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import Client as TestClient
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import ClientForm
from .models import Client


class ClientModelTest(TestCase):
    def test_valid_client_can_be_saved(self):
        client = Client.objects.create(
            full_name='Иван Петров',
            email='ivan@example.com',
            phone='+79990000001',
        )

        self.assertEqual(client.registration_date, timezone.localdate())
        self.assertIsNotNone(client.created_at)

    def test_full_name_cannot_be_empty(self):
        client = Client(full_name='   ', email='empty@example.com')

        with self.assertRaises(ValidationError) as context:
            client.full_clean()

        self.assertIn('full_name', context.exception.message_dict)

    def test_email_must_have_at_and_dot(self):
        client = Client(full_name='Иван Петров', email='invalid-email')

        with self.assertRaises(ValidationError) as context:
            client.full_clean()

        self.assertIn('email', context.exception.message_dict)

    def test_email_must_be_unique(self):
        Client.objects.create(full_name='Иван Петров', email='ivan@example.com')
        duplicate = Client(full_name='Петр Иванов', email='ivan@example.com')

        with self.assertRaises(ValidationError) as context:
            duplicate.full_clean()

        self.assertIn('email', context.exception.message_dict)

    def test_non_empty_phone_must_be_unique(self):
        Client.objects.create(
            full_name='Иван Петров',
            email='ivan@example.com',
            phone='+79990000001',
        )
        duplicate = Client(
            full_name='Петр Иванов',
            email='petr@example.com',
            phone='+79990000001',
        )

        with self.assertRaises(ValidationError) as context:
            duplicate.full_clean()

        self.assertIn('phone', context.exception.message_dict)

    def test_empty_phone_can_be_repeated(self):
        Client.objects.create(full_name='Иван Петров', email='ivan@example.com', phone='')
        Client.objects.create(full_name='Петр Иванов', email='petr@example.com', phone='')

        self.assertEqual(Client.objects.count(), 2)

    def test_registration_date_cannot_be_future(self):
        client = Client(
            full_name='Иван Петров',
            email='ivan@example.com',
            registration_date=timezone.localdate() + timedelta(days=1),
        )

        with self.assertRaises(ValidationError) as context:
            client.full_clean()

        self.assertIn('registration_date', context.exception.message_dict)


class ClientFormTest(TestCase):
    def test_form_is_valid_for_client_data(self):
        form = ClientForm(data={
            'full_name': 'Иван Петров',
            'email': 'ivan@example.com',
            'phone': '+79990000001',
            'registration_date': timezone.localdate().isoformat(),
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_form_rejects_future_registration_date(self):
        form = ClientForm(data={
            'full_name': 'Иван Петров',
            'email': 'ivan@example.com',
            'phone': '',
            'registration_date': (timezone.localdate() + timedelta(days=1)).isoformat(),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('registration_date', form.errors)


class ClientViewsTest(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.client_record = Client.objects.create(
            full_name='Иван Петров',
            email='ivan@example.com',
            phone='+79990000001',
        )

    def test_ping_endpoint(self):
        response = self.client.get('/clients/ping/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_clients_list(self):
        response = self.client.get(reverse('client_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иван Петров')

    def test_client_create(self):
        response = self.client.post(reverse('client_create'), {
            'full_name': 'Петр Иванов',
            'email': 'petr@example.com',
            'phone': '',
            'registration_date': timezone.localdate().isoformat(),
        })

        self.assertRedirects(response, reverse('client_list'))
        self.assertTrue(Client.objects.filter(email='petr@example.com').exists())

    def test_client_update(self):
        response = self.client.post(reverse('client_update', args=[self.client_record.pk]), {
            'full_name': 'Иван Сергеев',
            'email': 'ivan.sergeev@example.com',
            'phone': '+79990000002',
            'registration_date': self.client_record.registration_date.isoformat(),
        })

        self.assertRedirects(response, reverse('client_list'))
        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.full_name, 'Иван Сергеев')

    def test_client_delete(self):
        response = self.client.post(reverse('client_delete', args=[self.client_record.pk]))

        self.assertRedirects(response, reverse('client_list'))
        self.assertFalse(Client.objects.filter(pk=self.client_record.pk).exists())

    def test_missing_client_update_returns_404(self):
        response = self.client.get(reverse('client_update', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_missing_client_delete_returns_404(self):
        response = self.client.get(reverse('client_delete', args=[999]))

        self.assertEqual(response.status_code, 404)
