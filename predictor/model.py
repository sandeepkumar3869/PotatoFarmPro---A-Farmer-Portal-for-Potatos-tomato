import tensorflow as tf
import os

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
