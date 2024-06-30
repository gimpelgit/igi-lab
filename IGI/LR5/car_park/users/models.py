from django.db import models
from django.contrib.auth import get_user_model

from info.models import Vacancy
from system.models import Car

# Create your models here.
class Client(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=25, unique=True)
	date_of_birth = models.DateField()
	cars = models.ManyToManyField(Car, blank=True, related_name='clients')


class Employee(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=25, unique=True)
	salary = models.FloatField()
	date_of_birth = models.DateField()
	vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT)
	image = models.ImageField(upload_to='images/employees', blank=True)