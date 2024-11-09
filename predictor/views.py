from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image
import numpy as np
import os
from .forms import DiseasePredictionForm, CustomUserCreationForm, VegetableForm
from .model import Profile, Vegetable,CartItem, get_model
from .cart import Cart

def cart_view(request):
    cart = Cart(request)  # Initialize your cart
    cart_items = cart.get_items()  # Get the items in the cart
    total_amount = cart.get_total()  # Calculate the total amount
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def add_to_cart(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)

    cart = Cart(request)  # Initialize your cart
    cart.add(vegetable)  # Use the modified add method

    messages.success(request, f'{vegetable.name} has been added to your cart.')
    return redirect('shop')

def remove_from_cart(request, vegetable_id):
    cart = Cart(request)
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    cart.remove(vegetable)
    messages.success(request, f'{vegetable.name} has been removed from your cart.')
    return redirect('cart')

def shop_view(request):
    vegetables = Vegetable.objects.all()  
    return render(request, 'shop.html', {'vegetables': vegetables})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user,
                full_name=form.cleaned_data.get('full_name'),
                phone_number=form.cleaned_data.get('phone_number'),
                birth_date=form.cleaned_data.get('birth_date'),
                gender=form.cleaned_data.get('gender'),
                role=form.cleaned_data.get('role')
            )
            login(request, user)
            return redirect('farmer_portal' if profile.role == 'farmer' else 'home')
        print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login1(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        role = request.POST.get('role')  # Get the selected role from the form
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'profile') and user.profile.role == role:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}! You are now logged in.')
                redirect_page = 'farmer_portal' if user.profile.role == 'farmer' else 'home'
                return redirect(redirect_page)
            messages.error(request, 'Role mismatch or invalid role selected.')
        else:
            messages.error(request, 'Invalid username or password.')
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def farmer_portal(request):
    if request.method == 'POST':
        form = VegetableForm(request.POST)
        if form.is_valid():
            vegetable = form.save(commit=False)
            vegetable.farmer = request.user
            vegetable.save()
            return redirect('farmer_portal')
    else:
        form = VegetableForm()
    vegetables = Vegetable.objects.filter(farmer=request.user)
    return render(request, 'farmer_portal.html', {'form': form, 'vegetables': vegetables})

@login_required
def my_account(request):
    return render(request, 'my_account.html', {'profile': request.user.profile})

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

@login_required
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

def edit_vegetable(request, id):
    vegetable = get_object_or_404(Vegetable, id=id)
    if request.method == 'POST':
        form = VegetableForm(request.POST, instance=vegetable)
        if form.is_valid():
            form.save()
            return redirect('farmer_portal')  # Adjust this as needed
    else:
        form = VegetableForm(instance=vegetable)
    return render(request, 'edit_vegetable.html', {'form': form})
