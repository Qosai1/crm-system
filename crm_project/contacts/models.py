from django.db import models
from companies.models import Company


class Contact(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete = models.CASCADE,
        related_name='contacts'
    )
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name