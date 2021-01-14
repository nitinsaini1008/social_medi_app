from django import forms 
from .models import post_2,post_3

class post_2_form(forms.ModelForm):
	desc=forms.CharField(max_length=100)
	user_img=forms.ImageField()
	class Meta:
		model=post_2
		fields=['desc','user_img']

	def cleaned_naam(self):
		return self.cleaned_data['naam']

class post_3_form(forms.ModelForm):
	desc=forms.CharField(max_length=100)
	user_video=forms.FileField()
	class Meta:
		model=post_3
		fields=['desc','user_video']