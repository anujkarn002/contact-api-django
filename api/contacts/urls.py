from django.urls import re_path, include

from rest_framework_nested.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import ContactViewSet, PhoneViewSet, ContactLabelViewSet

contacts_router = SimpleRouter()
contacts_router.register(r'contacts', ContactViewSet)

phones_router = NestedSimpleRouter(contacts_router, r'contacts', lookup='contacts')
phones_router.register(r'phone', PhoneViewSet, basename='contacts-phone')

labels_router = NestedSimpleRouter(contacts_router, r'contacts', lookup='contacts')
labels_router.register(r'label', ContactLabelViewSet, basename='contacts-label')

urlpatterns = [
    re_path(r"", include(contacts_router.urls)),
    re_path(r"", include(phones_router.urls)),
    re_path(r"", include(labels_router.urls)),
]