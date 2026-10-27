from django.db import models
from companies.models import Company
from contacts.models import Contact
from django.conf import settings

class Deal(models.Model):
    STAGE_CHOICES = [
        ('new','New'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    title = models.CharField(max_length=100)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='deals'
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null= True,
        blank= True,
        related_name='deals',
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )
    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='new'
    )
    expected_close_date = models.DateField(
    null=True,
    blank=True
)
    assigned_to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assigned_deals',
    verbose_name='Assigned To'
)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title