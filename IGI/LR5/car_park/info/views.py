from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from system.models import Coupon
from users.models import Client, Employee
from .models import *
from .forms import ReviewForm
import requests
# Create your views here.


def index(request):
	article = Article.objects.latest('last_modification_date')	
	data = {'title': 'Главная страница', 'article': article}
	return render(request, 'info/index.html', context=data)


def about(request):
	company = Company.objects.first()
	return render(request, 'info/about.html', context={'company': company})


def privacy(request):
	data = {'title': 'Политика конфиденциальности'}
	return render(request, 'info/privacy.html', context=data)


def vacancy(request):
	vacancy = Vacancy.objects.all()
	data = {'vacancy': vacancy}
	return render(request, 'info/vacancy.html', context=data)


def reviews(request):
	reviews = Review.objects.all()
	data = {'title': 'Отзывы', 'reviews': reviews}
	return render(request, 'info/reviews.html', context=data)


@login_required
def add_review(request):
	if request.user.is_staff:
		return redirect('reviews')
	
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.client = Client.objects.get(user=request.user)
			review.save()
			return redirect('reviews')
	else:
		review = Review.objects.get(client=Client.objects.get(user=request.user))
		form = ReviewForm(instance=review) if review else ReviewForm()
	return render(request, 'info/add_review.html', {'form': form})


def contacts(request):
	employees = Employee.objects.all()
	data = {'title': 'Контакты', 'employees': employees}
	return render(request, 'info/contacts.html', context=data)


def promotions(request):
	coupons = Coupon.objects.all()
	data = {'title': 'Промокоды', 'coupons': coupons}
	return render(request, 'info/promotions.html', context=data)


def news(request):
	articles = Article.objects.all()
	data = {'title': 'Новости', 'articles': articles}
	return render(request, 'info/news.html', context=data)


def faq(request):
	faq = Faq.objects.all()
	return render(request, 'info/faq.html', context={'faq': faq})


def article(request, article_id):
	article = None
	try:
		article = Article.objects.get(id=article_id)
	except Exception:
		raise Http404()
	return render(request, 'info/article.html', context={'article': article})


@login_required
def random_dog_image(request):
	try:
		response = requests.get('https://dog.ceo/api/breeds/image/random')
		data = response.json()
		image_url = data['message']
		return render(request, 'info/random_dog.html', {'image_url': image_url})
	except:
		return render(request, 'info/check_internet_connection.html')


def page_not_found(request, exception=None):
	return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def no_access(request):
	return render(request, 'no_access.html')