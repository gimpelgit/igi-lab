from django.urls import path
from . import views

urlpatterns = [
	path('personal-cabinet/', views.personal_cabinet, name='personal-cabinet'),
	path('staff-cabinet/', views.staff_cabinet, name='staff-cabinet'),
	path('cars/', views.cars, name='cars'),
	path('car/add/<int:car_id>/', views.add_car, name='add-car'),
	path('car/delete/<int:car_id>/', views.delete_car, name='delete-car'),
	path('parking-space/<int:number>/', views.parking_space, name='parking-space'),
	path('parking-spaces/', views.parking_spaces, name='parking-spaces'),
	path('accrual/', views.accrual, name='accrual'),
	path('client-balance/', views.client_balance, name='client-balance'),
	path('client-payments/<int:client_id>/', views.client_payments, name='client-payments'),
	path('get-coupon/<int:coupon_id>/', views.get_coupon, name='get-coupon'),
	path('bank-cards/',views.bank_cards, name='bank-cards'),
	path('bank-cards/add/', views.add_bank_card, name='add-bank-card'),
	path('bank-cards/edit/<int:card_id>/', views.edit_bank_card, name='edit-bank-card'),
	path('bank-cards/delete/<int:card_id>/', views.delete_bank_card, name='delete-bank-card'),
]