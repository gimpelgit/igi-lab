from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Client

from .forms import LoginForm, RegisterForm


# Create your views here.

class LoginUser(LoginView):
	form_class = LoginForm
	template_name = 'users/login.html'
	extra_context = {'title': 'Авторизация'}


def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('index'))
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = form.save(commit=False)
			user.set_password(cd['password1'])

			user.first_name = cd['first_name']
			user.last_name = cd['last_name']
			user.email = cd['email']
			user.save()
			client = Client(
				user=user,
				phone_number=cd['phone_number'],
				date_of_birth=cd["date_of_birth"]
			)
			client.save()

			return HttpResponseRedirect(reverse('login'))	
	else:
		form = RegisterForm()
	return render(request, 'users/register.html', {'form': form})
	

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))	

