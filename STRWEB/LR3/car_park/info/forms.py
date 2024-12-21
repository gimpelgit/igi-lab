from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['body', 'grade']
		labels = {
			'body': 'Сообщение',
			'grade': 'Оценка',
		}
	
	def clean_grade(self):
		grade = self.cleaned_data['grade']
		if grade < 1 or grade > 5:
			raise forms.ValidationError('Оценка должна быть 1, 2, 3, 4 или 5')
		return grade 