
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    subscription = forms.ChoiceField(
        choices=CustomUser.SUBSCRIPTIONS,
        label="مدة الاشتراك"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'subscription', 'password1', 'password2']

class CardForm(forms.Form):
    network_name = forms.CharField(label="اسم الشبكة", max_length=100)
    login_page = forms.CharField(label="رابط صفحة الدخول", max_length=100)
    support_phone = forms.CharField(label="رقم الدعم الفني", max_length=20)
    excel_file = forms.FileField(label="ملف Excel")
    format_choice = forms.ChoiceField(label="نوع التصدير", choices=[('html', 'HTML'), ('pdf', 'PDF')])
