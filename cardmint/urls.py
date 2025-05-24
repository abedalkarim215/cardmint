
from django.contrib import admin
from django.urls import path
from generator import views as gen_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='generator/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', gen_views.register_view, name='register'),
    path('blocked/', gen_views.blocked_view, name='blocked'),
    path('', gen_views.generate_cards, name='home'),
]
