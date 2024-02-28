from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, help_text='Имя(Ник)')
    mail = models.EmailField(help_text='Электронная почта', null=True, blank=True)
    phone = models.CharField(max_length=20, help_text='Телефон')
