from django import forms

class DiseasePredictionForm(forms.Form):
    MODEL_CHOICES = [
        ('potato', 'Potato Disease'),
        ('tomato', 'Tomato Disease'),
    ]
    
    model_type = forms.ChoiceField(choices=MODEL_CHOICES, label='Select Crop')
    image = forms.ImageField(label='Upload Leaf Image')
