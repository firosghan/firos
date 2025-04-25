from django import forms

from.models import *


class normalform(forms.Form):
    name=forms.CharField(max_length=20)
    price=forms.IntegerField()
    quantity=forms.IntegerField()
    image=forms.ImageField()

class modelform(forms.ModelForm):
    class Meta:
        model=product
        fields = '__all__'

class Profile(forms.ModelForm):
    class Meta:
        model=user_resgister
        fields = '__all__'