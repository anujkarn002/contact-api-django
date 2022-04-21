from django.urls import reverse

from core.tests import BaseAPITestCase

from .models import Contact, Phone


class ContactsAPITestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()

    def create_contact(self, user):
        new_contact = Contact.objects.create(
            first_name="Test", middle_name="Middle", last_name="Last", email="test@roger.com",
            user_id=user.id)
        new_contact.phones.create(number="8090872323")
        new_contact.labels.create(name="Mobile")
        return new_contact

    def test_user_can_create_contact(self):
        """
        Test that a user can create contact
        """
        url = reverse('contact-list')
        data = {
            "first_name": "Test",
            "middle_name": "Middle",
            "last_name": "Last",
            "phones": [
                {
                    "number": "8090872323",
                }
            ],
            "labels": [],
            "email": "test@contact.com",
        }
        response = self.roger_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_can_edit_contact(self):
        """
        Test that a user can edit contact
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse('contact-detail', kwargs={'pk': test_contact.id})
        data = {
            "first_name": "Test",
            "middle_name": "Middle",
            "last_name": "Last",
            "phones": [
                {
                    "number": "8090872327",
                }
            ]
        }
        response = self.roger_client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_contact(self):
        """
        Test that a user can delete contact
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse('contact-detail', kwargs={'pk': test_contact.id})
        response = self.roger_client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)

    def test_user_can_get_contact_list(self):
        """
        Test that a user can get contact list
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse('contact-list')
        response = self.roger_client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'].get('count'), 1)


class PhonesAPITestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()

    def create_contact(self, user):
        new_contact = Contact.objects.create(
            first_name="Test", middle_name="Middle", last_name="Last", email="test@roger.com",
            user_id=user.id)
        new_contact.phones.create(number="8090872323")
        return new_contact

    def test_user_can_create_phone(self):
        """
        Test that a user can create phone
        """
        new_contact = self.create_contact(self.roger_user)
        url = reverse('contacts-phone-list',
                      kwargs={'contacts_pk': new_contact.id})
        data = {
            "number": "8090872323",
        }
        response = self.roger_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_can_edit_phone(self):
        """
        Test that a user can edit phone
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse(
            'contacts-phone-detail', kwargs={'contacts_pk': test_contact.id, 'pk': test_contact.phones.first().id})
        data = {
            "number": "8090872327",
        }
        response = self.roger_client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_phone(self):
        """
        Test that a user can delete phone
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse('contacts-phone-detail',
                      kwargs={'contacts_pk': test_contact.id, 'pk': test_contact.phones.first().id})
        response = self.roger_client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)


class ContactLabelsAPITestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()

    def create_contact(self, user):
        new_contact = Contact.objects.create(
            first_name="Test", middle_name="Middle", last_name="Last", email="test@roger.com",
            user_id=user.id)
        new_contact.labels.create(name="Friend")
        return new_contact

    def test_user_can_create_label(self):
        """
        Test that a user can create label
        """
        new_contact = self.create_contact(self.roger_user)
        url = reverse('contacts-label-list',
                      kwargs={'contacts_pk': new_contact.id})
        data = {
            "name": "Family",
        }
        response = self.roger_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_can_edit_label(self):
        """
        Test that a user can edit label
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse(
            'contacts-label-detail', kwargs={'contacts_pk': test_contact.id, 'pk': test_contact.labels.first().id})
        data = {
            "name": "Group 2",
        }
        response = self.roger_client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_label(self):
        """
        Test that a user can delete label
        """
        test_contact = self.create_contact(self.roger_user)
        url = reverse('contacts-label-detail',
                      kwargs={'contacts_pk': test_contact.id, 'pk': test_contact.labels.first().id})
        response = self.roger_client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
