from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q

from system.models import Coupon
from users.models import Client, Employee
from .models import *
from .forms import ReviewForm
import requests
# Create your views here.

User = get_user_model()


def task7(request):
    return render(request, 'info/task7.html')

def task8(request):
    return render(request, 'info/task8.html')

def task9(request):
    return render(request, 'info/task9.html')


def index(request):
    article = Article.objects.latest('last_modification_date')	
    companies = Company.objects.filter(id__gt=1)
    data = {'title': 'Главная страница', 'article': article, 'companies': companies}
    return render(request, 'info/index.html', context=data)


def about(request):
    history = CompanyHistory.objects.all()
    return render(request, 'info/about.html', context={'history': history})


def privacy(request):
    data = {'title': 'Политика конфиденциальности'}
    return render(request, 'info/privacy.html', context=data)


def vacancy(request):
    vacancy = Vacancy.objects.all()
    data = {'vacancy': vacancy}
    return render(request, 'info/vacancy.html', context=data)


def reviews(request):
    reviews = Review.objects.all()
    add = True
    if request.user.is_authenticated and not request.user.is_staff:
        try:
            review = request.user.client.review
            add = False
        except Review.DoesNotExist:
            pass
    data = {'title': 'Отзывы', 'reviews': reviews, 'add': add}
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

@login_required
def update_review(request):
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
    return render(request, 'info/update_review.html', {'form': form})


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


def employee_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'info/employee_list.html', {'vacancies': vacancies})


def contact_details(request, id):
    employee = Employee.objects.get(id=id)
    
    data = {
        'name': f"{employee.user.first_name} {employee.user.last_name}",
        'phone_number': employee.phone_number,
        'email': employee.user.email,
        'image_url': employee.image.url if employee.image else None,
        'vacancy_name': employee.vacancy.name,
        'id': employee.id
    }
    return JsonResponse(data)

def table_contacts(request):
    employees = Employee.objects.all()

    # Сортировка
    sort_by = request.GET.get('sort_by', 'user')
    if sort_by:
        employees = employees.order_by(sort_by)

    query = request.GET.get('search', '')
    if query:
        employees = employees.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(phone_number__icontains=query) |
        Q(user__email__icontains=query)
    )
        
    paginator = Paginator(employees, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'employees': [
            {
                'name': f"{employee.user.first_name} {employee.user.last_name}",
                'phone_number': employee.phone_number,
                'email': employee.user.email,
                'id': employee.id
            }
            for employee in page_obj
        ],
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'page_number': page_obj.number,
        'num_pages': page_obj.paginator.num_pages
    }

    return JsonResponse(data)



def add_employee(request):
    if request.method == 'POST':
        # Получаем данные из формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        salary = request.POST.get('salary')
        date_of_birth = request.POST.get('date_of_birth')
        vacancy_id = request.POST.get('vacancy')
        image = request.FILES.get('image')

        try:
            # Создаем нового пользователя
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=make_password(password)  # Хэшируем пароль
            )
            # Получаем вакансию
            vacancy = Vacancy.objects.get(id=vacancy_id)

            if image:
                file_name = default_storage.get_available_name(image.name)
                file_path = f'images/employees/{file_name}'

                # Сохраняем файл
                file_content = ContentFile(image.read())
                default_storage.save(file_path, file_content)

            else:
                file_path = f'images/employees/default-employee.png'
            
            # Создаем сотрудника
            Employee.objects.create(
                user=user,
                phone_number=phone_number,
                salary=salary,
                date_of_birth=date_of_birth,
                vacancy=vacancy,
                image=file_path
            )

            return JsonResponse({'success': True, 'message': 'Сотрудник успешно добавлен.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'})


def page_not_found(request, exception=None):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def no_access(request):
    return render(request, 'no_access.html')