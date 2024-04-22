from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page),

    path('upload/', views.upload_image, name='upload_image'),
    path('decrypt/<int:image_id>/', views.decrypt_image, name='decrypt_image'),
    path('manual-decryption/', views.manual_decryption, name='manual_decryption'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('decryptbyid/',views.decryptbyid),
]
