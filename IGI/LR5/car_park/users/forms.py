from datetime import date
import re
from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Логин', widget=forms.TextInput())
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
	username = forms.CharField(label='Логин', widget=forms.TextInput())
	first_name = forms.CharField(label='Имя', widget=forms.TextInput())
	last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
	email = forms.CharField(label='Почта', widget=forms.TextInput())
	phone_number = forms.CharField(label="Номер телефона", widget=forms.TextInput())
	date_of_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(
		attrs={
			'class':'form',
			'type':'date'
		}
	))
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())


	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']
		if not re.match(r"^\+375 \(\d{2,3}\) \d\d\d-\d\d-\d\d$", phone_number):
			raise forms.ValidationError('Номер телефона должен соответствовать формату +375 (XX) XXX-XX-XX')
		return phone_number

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError('Пароли не совпадают')
		return cd['password1']
	

	def clean_email(self):
		email = self.cleaned_data['email']
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			raise forms.ValidationError('Некорректный адрес электронной почты')
		if get_user_model().objects.filter(email=email).exists():
			raise forms.ValidationError('Такой email уже существует')
		return email
	

	def clean_date_of_birth(self):
		date_of_birth = self.cleaned_data.get('date_of_birth')
		today = date.today()
		age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
		if age < 18:
			raise forms.ValidationError('Вам должно быть не менее 18 лет')
		return date_of_birth