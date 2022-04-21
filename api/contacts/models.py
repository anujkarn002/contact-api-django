from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    '''
    Contact model - represents a contact in the database
    '''
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(_("First Name"), max_length=255)
    middle_name = models.CharField(
        _("Middle Name"), max_length=255, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, null=True, blank=True)
    image = models.URLField(_("Image"), null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    is_favorite = models.BooleanField(_("Is Favorite"), default=False)
    address = models.TextField(_("Address"), null=True, blank=True)
    note = models.TextField(_("Notes"), null=True, blank=True)
    job_title = models.CharField(_("Job Title"), max_length=50, null=True, blank=True)
    current_company = models.CharField(_("Current Company"), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Phone(models.Model):
    '''
    Phone model - represents a phone number for a contact in the database
    '''
    contact = models.ForeignKey(
        'contacts.Contact', on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(_("Number"), max_length=50)
    country_code = models.CharField(_("Country Code"), max_length=50, null=True, blank=True)
    label = models.CharField(_("Label"), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.number


class ContactLabel(models.Model):
    '''
    ContactLabel model - represents a labels for a contact in the database
    '''
    contact = models.ForeignKey(
        'contacts.Contact', on_delete=models.CASCADE, related_name='labels')
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

