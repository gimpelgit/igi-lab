from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('no-access/', views.no_access, name='no-access'),
	path('about/', views.about, name='about'),
	path('privacy/', views.privacy, name='privacy'),
	path('vacancy/', views.vacancy, name='vacancy'),
	path('reviews/', views.reviews, name='reviews'),
	path('contacts/', views.contacts, name='contacts'),
	path('news/', views.news, name='news'),
	path('promotions/', views.promotions, name='promotions'),
	path('faq/', views.faq, name='faq'),
	path('article/<int:article_id>/', views.article, name='article'),
	path('add-review/', views.add_review, name='add-review'),
	path('update-review/', views.update_review, name='update-review'),
	path('random-dog/', views.random_dog_image, name='random-dog'),
    
	path('employee-list/', views.employee_list, name='employee-list'),
	path('add-employee/', views.add_employee, name='add-employee'),
	path('table-contacts/', views.table_contacts, name='table-contacts'),
	path('contact-details/<int:id>/', views.contact_details, name='contact-details'),
	
    
    path('task7/', views.task7, name='task7'),
    path('task8/', views.task8, name='task8'),
    path('task9/', views.task9, name='task9'),
]