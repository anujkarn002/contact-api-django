
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from core.utils import success_response
from core.pagination import DefaultResultsSetPagination

from .filters import ContactFilter
from .models import Contact, ContactLabel, Phone
from .serializers import ContactLabelSerializer, ContactSerializer, PhoneSerializer


class ContactViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    pagination_class = DefaultResultsSetPagination
    filterset_class = ContactFilter

    def get_paginated_response(self, data, detail=None):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data=data, detail=detail)

    def get_user_queryset(self):
        queryset = self.queryset
        queryset = queryset.objects.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context=self.get_serializer_context())
        return self.paginator.get_paginated_response(detail="Fetched all contacts" if page != [] else "No contacts found", data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(detail='Successfully created a new contact.', code=status.HTTP_201_CREATED, **serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return success_response(detail='Successfully updated contact.', code=status.HTTP_200_OK, **serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(detail='Successfully deleted contact.', code=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(detail='Successfully retrieved contact.', code=status.HTTP_200_OK, **serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def search(self, request, *args, **kwargs):
        query = request.GET.get('q', None)
        if query is None:
            raise exceptions.ValidationError('Please provide a query.')
        queryset = self.get_queryset()
        queryset = queryset.filter(first_name__icontains=query)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context=self.get_serializer_context())
        return self.paginator.get_paginated_response(detail="Fetched all contacts" if page != [] else "No contacts found", data=serializer.data)


class ContactLabelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ContactLabel.objects.all()
    serializer_class = ContactLabelSerializer
    pagination_class = DefaultResultsSetPagination

    def get_paginated_response(self, data, detail=None):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data=data, detail=detail)

    def filter_queryset(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = self.queryset.filter(contact=self.kwargs['contacts_pk'])
        return queryset

    def get_object(self):
        return self.get_object_queryset().first()

    def get_object_queryset(self):
        queryset = self.filter_queryset(
            self.get_queryset())
        phone_pk = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, Q(pk=phone_pk))
        # TODO - May raise a permission denied
        # self.check_object_permissions(self.request, obj)
        return queryset.filter(Q(pk=phone_pk))

    def create(self, request, *args, **kwargs):
        contact = get_object_or_404(Contact, Q(pk=self.kwargs['contacts_pk']))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_phone = contact.labels.create(**serializer.validated_data)
        serializer = self.get_serializer(new_phone)
        return success_response(detail='Successfully added new label.', code=status.HTTP_201_CREATED, **serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return success_response(detail='Successfully updated label.', code=status.HTTP_200_OK, **serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(detail='Successfully deleted label.', code=status.HTTP_204_NO_CONTENT)


class PhoneViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    pagination_class = DefaultResultsSetPagination

    def get_paginated_response(self, data, detail=None):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data=data, detail=detail)

    def filter_queryset(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = self.queryset.filter(contact=self.kwargs['contacts_pk'])
        return queryset

    def get_object(self):
        return self.get_object_queryset().first()

    def get_object_queryset(self):
        queryset = self.filter_queryset(
            self.get_queryset())
        phone_pk = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, Q(pk=phone_pk))
        # TODO - May raise a permission denied
        # self.check_object_permissions(self.request, obj)
        return queryset.filter(Q(pk=phone_pk))

    def create(self, request, *args, **kwargs):
        contact = get_object_or_404(Contact, Q(pk=self.kwargs['contacts_pk']))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_phone = contact.phones.create(**serializer.validated_data)
        serializer = self.get_serializer(new_phone)
        return success_response(detail='Successfully added new phone number.', code=status.HTTP_201_CREATED, **serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return success_response(detail='Successfully updated phone number.', code=status.HTTP_200_OK, **serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(detail='Successfully deleted phone number.', code=status.HTTP_204_NO_CONTENT)
