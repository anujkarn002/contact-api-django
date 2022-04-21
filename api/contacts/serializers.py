from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Contact, Phone, ContactLabel


class ContactLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactLabel
        fields = ['id', 'name']
        read_only_fields = ['id']


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['id', 'number', 'country_code', 'label']
        read_only_fields = ['id']


class ContactSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField(read_only=True)
    phones = serializers.SerializerMethodField(read_only=True)

    def get_labels(self, obj):
        label_serializer = ContactLabelSerializer(obj.labels, many=True)
        return label_serializer.data
    def get_phones(self, obj):
        phone_serializer = PhoneSerializer(obj.phones, many=True)
        return phone_serializer.data

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'first_name', 'middle_name', 'last_name', 'address',
                  'email', 'image', 'note', 'job_title', 'current_company', 'is_favorite',
                  'phones', 'labels']
        read_only_fields = ('id', 'labels', 'phones')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        phones = self.initial_data.pop('phones', [])
        labels = self.initial_data.pop('labels', [])
        contact = super().create(validated_data)
        for phone in phones:
            if phone.get('number'):
                Phone.objects.create(contact=contact, **phone)
        for label in labels:
            if label.get('name'):
                ContactLabel.objects.get_or_create(name=label.get('name'), contact=contact)
        return contact

    def update(self, instance, validated_data):
        phones = self.initial_data.pop('phones', [])
        labels = self.initial_data.pop('labels', [])
        updated_contact = super().update(instance, validated_data)
        for phone in phones:
            if phone.get('number'):
                Phone.objects.create(contact=updated_contact, **phone)
        for label in labels:
            if label.get('name'):
                ContactLabel.objects.get_or_create(name=label.get('name'), contact=updated_contact)
        return updated_contact
