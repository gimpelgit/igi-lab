from django.db import models


# Create your models here.
class Car(models.Model):
	name = models.CharField(max_length=100)
	number = models.CharField(max_length=15)
	model = models.CharField(max_length=100)
	brand = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class BankCard(models.Model):
	client = models.ForeignKey('users.Client', on_delete=models.CASCADE)
	card_number = models.CharField(max_length=16)
	expiry_date = models.DateField()
	cvv = models.CharField(max_length=3)

	def __str__(self):
		return "*" * (len(self.card_number) - 4) + self.card_number[-4:]


class Accrual(models.Model):
	client = models.ForeignKey('users.Client', on_delete=models.CASCADE)
	bank_card = models.ForeignKey(BankCard, null=True, on_delete=models.SET_NULL)
	amount = models.FloatField()
	date = models.DateField(auto_now_add=True)


class Payment(models.Model):
	client = models.ForeignKey('users.Client', on_delete=models.CASCADE)
	payment_date = models.DateField(auto_now_add=True)
	reservation_start_date = models.DateField()
	reservation_end_date = models.DateField()
	total_cost = models.FloatField()
	car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
	coupon_client = models.ForeignKey('CouponClient', null=True, blank=True, on_delete=models.SET_NULL)
	number_parking_space = models.IntegerField()


class ParkingSpace(models.Model):
	client = models.ForeignKey('users.Client', null=True, blank=True, on_delete=models.SET_NULL)
	number = models.IntegerField(primary_key=True, unique=True)
	cost_per_day = models.FloatField()
	image = models.ImageField(upload_to='images/parking_spaces', blank=True)


class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True)
	discount_type = models.CharField(max_length=10, choices=[('percent', 'Процент'), ('amount', 'Сумма')])
	discount_value = models.FloatField()
	min_amount = models.FloatField(default=0)
	price = models.FloatField(default=0)
	start_date = models.DateField()
	end_date = models.DateField()
	clients = models.ManyToManyField('users.Client', related_name='coupons', through='CouponClient')

	def __str__(self):
		discount_type_text = "%" if self.discount_type == 'percent' else " BYN"
		return (f"Купон на скидку в {self.discount_value}{discount_type_text} "
			f"на минимальную сумму в {self.min_amount} BYN. " 
			f"Действует в период с {self.start_date} до {self.end_date}")


class CouponClient(models.Model):
	client = models.ForeignKey('users.Client', on_delete=models.CASCADE)
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	is_used = models.BooleanField(default=False)

	def __str__(self):
		return self.coupon.__str__()