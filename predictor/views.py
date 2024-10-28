from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
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
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}. You can now login.')
            return redirect('login1')
        else:
            messages.error(request, 'An error occurred during registration. Please try again.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# Login view
def login1(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}! You are now logged in.')
                return redirect('home')  # Redirect to the homepage or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('home')


def home_view(request):
    return render(request, 'index.html')



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
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def contact(request):
    return render(request, 'contact-us.html')

def gallery(request):
    return render(request, 'gallery.html')

@login_required
def my_account(request):
    return render(request, 'my_account.html')

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224)).convert('RGB')
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
            
            classes = {
                'potato': ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy'],
                'tomato': ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 
                           'Tomato_Bacterial_spot', 'Tomato_Early_blight', 
                           'Tomato_Late_blight', 'Tomato_Leaf_Mold', 
                           'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
                           'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
                           'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
            }.get(model_type)

            if classes is None:
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
