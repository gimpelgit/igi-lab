from .models import Company

def company_processor(request):
	company = Company.objects.get(id=1)
	return {'main_company': company}  