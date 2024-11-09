import tensorflow as tf
import os
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    role = models.CharField(max_length=10, choices=[('farmer', 'Farmer'), ('customer', 'Customer')], blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# Dictionary to store loaded models
_models = {}

def get_model(model_type):
    """
    Loads and returns the model corresponding to the given model_type.
    Caches the model after loading for faster subsequent access.
    """
    if model_type in _models:
        return _models[model_type]
    else:
        model_path = os.path.join(os.path.dirname(__file__), 'models')
        if model_type == 'potato':
            model_file = os.path.join(model_path, 'potato_model.keras')
        elif model_type == 'tomato':
            model_file = os.path.join(model_path, 'tomato_model.keras')
        else:
            raise ValueError("Invalid model type")
        
        model = tf.keras.models.load_model(model_file)
        _models[model_type] = model
        return model

class Vegetable(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the farmer
    name = models.CharField(max_length=100)  # Name of the vegetable
    quantity = models.PositiveIntegerField()  # Available quantity
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.vegetable.name} (x{self.quantity})'