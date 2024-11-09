from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from predictor.model import Profile, Vegetable

class DiseasePredictionForm(forms.Form):
    MODEL_CHOICES = [
        ('potato', 'Potato Disease'),
        ('tomato', 'Tomato Disease'),
    ]
    
    model_type = forms.ChoiceField(choices=MODEL_CHOICES, label='Select Crop')
    image = forms.ImageField(label='Upload Leaf Image')

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    role = forms.ChoiceField(choices=[('farmer', 'Farmer'), ('customer', 'Customer')], required=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone_number', 'birth_date', 'gender', 'role', 'password1', 'password2')

class VegetableForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ['name', 'quantity', 'price']