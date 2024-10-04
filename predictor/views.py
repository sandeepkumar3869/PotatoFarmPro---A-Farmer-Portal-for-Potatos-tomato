
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.views import LogoutView as AuthLogoutView
from .forms import DiseasePredictionForm
from .model import get_model
from PIL import Image
import numpy as np
import os
from django.core.files.storage import default_storage
from django.conf import settings


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'predictor/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'predictor/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'predictor/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        return render(request, 'predictor/login.html', {'form': form})

class LogoutView(AuthLogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')  # Redirect to home after logout

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
def services(request):
    return render(request, 'services.html')
def shop(request):
    return render(request, 'shop.html') 
def shop_detail(request):
    return render(request, 'shop-detail.html')
def cart(request):
    # Here you can handle cart logic, like displaying cart items
    return render(request, 'cart.html')
def checkout(request):
    # Here you can handle the checkout process
    return render(request, 'checkout.html')
def wishlist(request):
    # Here you can implement the logic for displaying the user's wishlist.
    return render(request, 'wishlist.html')
def contact(request):
    return render(request, 'contact-us.html')

def gallery(request):
    # Here you can implement the logic for displaying the gallery.
    return render(request, 'gallery.html')


@login_required  # Ensure the user is logged in to access this view
def my_account(request):
    return render(request, 'my_account.html')
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img = img.convert('RGB')
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_disease(request, model_type):
    if request.method == 'POST':
        form = DiseasePredictionForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = default_storage.save(os.path.join('uploads', image.name), image)
            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            processed_image = preprocess_image(full_image_path)

            model = get_model(model_type)
            prediction = model.predict(processed_image)
            predicted_class = np.argmax(prediction, axis=1)[0]
            confidence = np.max(prediction) * 100
            
            if model_type == 'potato':
                classes = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
            elif model_type == 'tomato':
                classes = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Tomato_Bacterial_spot',
                           'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
                           'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
                           'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
                           'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
            else:
                return render(request, 'predictor/predict.html', {'form': form, 'error': 'Invalid model type'})

            result = classes[predicted_class]
            context = {
                'result': result,
                'confidence': round(confidence, 2),
                'image_url': default_storage.url(image_path),
                'model_type': model_type 
            }
            return render(request, 'predictor/result.html', context)
    else:
        form = DiseasePredictionForm()
    return render(request, 'predictor/predict.html', {'form': form, 'model_type': model_type})





# Other existing views...
