import re
from django import forms
from .models import Accrual, BankCard, Car, CouponClient, Payment
from datetime import datetime
from django.utils import timezone

class EditCarForm(forms.ModelForm):
	number = forms.CharField(label='Рег. знак', widget=forms.TextInput())

	class Meta:
		model = Car
		fields = ['name', 'number', 'model', 'brand']
		labels = {
			'name': 'Название',
			'model': 'Модель',
			'brand': 'Марка',
		}

	def clean_number(self):
		number = self.cleaned_data['number']
		if not re.match(r"^\d{4}[ABEIKMHOPCTX]{2}-\d$", number):
			raise forms.ValidationError('Некорректный регистрационный знак')
		return number


class PaymentForm(forms.ModelForm):
	reservation_start_date = forms.DateField(label='Начало брони', widget=forms.DateInput(
		attrs={
			'type':'date'
		}
	))
	reservation_end_date = forms.DateField(label='Конец брони', widget=forms.DateInput(
		attrs={
			'type':'date'
		}
	))

	class Meta:
		model = Payment
		fields = ['reservation_start_date', 'reservation_end_date', 'car', 'coupon_client']
		labels = {
			'car': 'Машина',
			'coupon_client': 'Купон'
		}


	def __init__(self, client, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['car'] = forms.ModelChoiceField(queryset=client.cars.all())
		self.fields['coupon_client'] = forms.ModelChoiceField(queryset=self.get_coupons(client), required=False)


	def get_coupons(self, client):
		return CouponClient.objects.filter(
			client=client,
			coupon__start_date__lte=timezone.now().date(),
			coupon__end_date__gte=timezone.now().date(),
			is_used=False
		).all()


	def clean_reservation_end_date(self):
		start = self.cleaned_data['reservation_start_date']
		end = self.cleaned_data['reservation_end_date']
		if start > end:
			raise forms.ValidationError('Неправильный промежуток времени')
		return end 


class AccrualForm(forms.ModelForm):
	amount = forms.FloatField(label='Сумма пополнения')
	bank_card = forms.ModelChoiceField(queryset=None, label='Банковская карта')
	
	class Meta:
		model = Accrual
		fields = ['bank_card', 'amount']

	def __init__(self, client, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['bank_card'].queryset = client.bankcard_set.all()


class MonthYearWidget(forms.MultiWidget):
	def __init__(self, attrs=None):
		months = [(i, '{:02d}'.format(i)) for i in range(1, 13)]
		years = [(i, str(i)) for i in range(datetime.now().year - 6, datetime.now().year + 1)]
		widgets = [
			forms.Select(attrs=attrs, choices=months),
			forms.Select(attrs=attrs, choices=years),
		]
		super().__init__(widgets, attrs)


	def decompress(self, value):
		if value:
			if isinstance(value, datetime):
				value = value.date()
			if isinstance(value, str):
				date = datetime.strptime(value, "%Y-%m-%d")
			else:
				date = value
			return [date.month, date.year]
		return [None, None]


class MonthYearField(forms.MultiValueField):
	def __init__(self, *args, **kwargs):
		fields = (
			forms.IntegerField(),
			forms.IntegerField(),
		)
		super().__init__(fields, widget=MonthYearWidget(), *args, **kwargs)


	def compress(self, data_list):
		if data_list:
			return datetime(year=data_list[1], month=data_list[0], day=1).date()
		return None


class BankCardForm(forms.ModelForm):
	expiry_date = MonthYearField(label='Действует до')

	class Meta:
		model = BankCard
		fields = ['card_number', 'expiry_date', 'cvv']
		labels = {
			'card_number': 'Номер карточки',
		}

	def clean_card_number(self):
		card_number = self.cleaned_data['card_number']
		if not re.match(r'^\d{16}$', card_number):
			raise forms.ValidationError('Некорректный номер карты')
		return card_number
		