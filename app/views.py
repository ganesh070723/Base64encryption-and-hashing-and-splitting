# views.py

import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import EncodedImage
import os
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return HttpResponse("User created successfully. Please <a href='/login'>login</a>.")
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Invalid login credentials.")
    return render(request, 'registration/login.html')
@login_required
def home_page(request):
    return render(request, 'home-page.html')
@login_required
def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            half_length = len(encoded_image) // 2
            part_a = encoded_image[:half_length]
            part_b = encoded_image[half_length:]

            # Save A.txt and B.txt
            image_id = EncodedImage.objects.latest('id').id + 1 if EncodedImage.objects.exists() else 1
            file_path_a = os.path.join(settings.MEDIA_ROOT, f'{image_id}A.txt')
            file_path_b = os.path.join(settings.MEDIA_ROOT, f'{image_id}B.txt')
            with open(file_path_a, 'w') as f:
                f.write(part_a)
            with open(file_path_b, 'w') as f:
                f.write(part_b)

            # Save to database
            EncodedImage.objects.create(user=request.user, part_a=part_a, part_b=part_b)

            return render(request, 'upload_success.html', {'id': image_id})
    return render(request, 'upload_image.html')
# def upload_image(request):
#     if request.method == 'POST':
#         image_file = request.FILES['image']
#         encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
#         half_length = len(encoded_image) // 2
#         part_a = encoded_image[:half_length]
#         part_b = encoded_image[half_length:]
#         encoded_image_obj = EncodedImage.objects.create(part_a=part_a, part_b=part_b)
#         return render(request, 'upload_success.html', {'id': encoded_image_obj.id})
#     return render(request, 'upload_image.html')

def keyhashing(request):
    pass
@login_required
def decrypt_image(request, image_id):
    encoded_image = get_object_or_404(EncodedImage, pk=image_id)

    # Check if the current user has permission to access the image
    if encoded_image.user != request.user:
        return render(request,'404.html')

    full_encoded_image = encoded_image.part_a + encoded_image.part_b
    decoded_image = base64.b64decode(full_encoded_image)
    return render(request, 'decrypt_image.html', {'image_data': full_encoded_image})
# def decrypt_image(request, image_id):
#     encoded_image = get_object_or_404(EncodedImage, pk=image_id)
#     full_encoded_image = encoded_image.part_a + encoded_image.part_b
#     decoded_image = base64.b64decode(full_encoded_image)
#     # print(decoded_image)
#     return render(request, 'decrypt_image.html', {'image_data': full_encoded_image})
# def decrypt_image(request, image_id):
#     encoded_image = get_object_or_404(EncodedImage, pk=image_id)
#     full_encoded_image = encoded_image.part_a + encoded_image.part_b
#     decoded_image = base64.b64decode(full_encoded_image)
#     return HttpResponse(decoded_image, content_type="image/jpeg")
@login_required
def manual_decryption(request):
    if request.method == 'POST':
        part_a = request.POST['part_a']
        part_b = request.POST['part_b']
        full_encoded_image = part_a + part_b
        c = full_encoded_image
        a=base64.b64decode(c)
        return render(request, 'manual_decryption.html', {'image_data': full_encoded_image})
    return render(request, 'manual_decryption_form.html')

# def manual_decryption(request):
#     if request.method == 'POST':
#         part_a = request.POST.get('part_a')
#         part_b = request.POST.get('part_b')
#         if part_a and part_b:
#             full_encoded_image = part_a + part_b
#             try:
#                 decoded_image = base64.b64decode(full_encoded_image)
#                 return render(request, 'manual_decryption.html', {'image_data': decoded_image})
#             except Exception as e:
#                 error_message = f"Error decoding image: {str(e)}"
#                 return render(request, 'manual_decryption.html', {'error_message': error_message})
#         else:
#             error_message = "Both A and B parts are required."
#             return render(request, 'manual_decryption.html', {'error_message': error_message})
#     return render(request, 'manual_decryption_form.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')

def decryptbyid(request):
    if request.method == 'POST':
        username = request.POST['decryptid']
        return redirect(f'/decrypt/{username}')
    return render(request,'decryptbyid.html')