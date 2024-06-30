from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Article)
admin.site.register(Faq)
admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Review)