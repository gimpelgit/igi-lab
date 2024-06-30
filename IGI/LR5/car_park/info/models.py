from django.db import models


# Create your models here.
class Company(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)


class Faq(models.Model):
	question = models.CharField(max_length=255)
	answer = models.TextField(blank=True)

class Vacancy(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class Article(models.Model):
	title = models.CharField(max_length=255)
	summary = models.CharField(max_length=255)
	body = models.TextField(blank=True)
	image = models.ImageField(upload_to='images/articles', blank=True)
	last_modification_date = models.DateTimeField(auto_now=True)


class Review(models.Model):
	client = models.OneToOneField('users.Client', primary_key=True, on_delete=models.CASCADE)
	grade = models.IntegerField()
	body = models.TextField()
	