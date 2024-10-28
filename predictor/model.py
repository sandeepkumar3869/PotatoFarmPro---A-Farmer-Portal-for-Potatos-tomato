import tensorflow as tf
import os
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
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
