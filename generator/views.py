
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CardForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from datetime import timedelta
from django.utils import timezone
import os

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_mail(
                subject="🆕 طلب تسجيل مستخدم جديد",
                message=f"تم تسجيل المستخدم: {user.username}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["abedalkarim215@gmail.com"],
            )

            messages.success(request, "تم التسجيل بنجاح. سنراجع طلبك ونتواصل معك بشأن الدفع.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "generator/register.html", {"form": form})

@login_required
def generate_cards(request):
    user = request.user
    if not user.approved or user.is_expired():
        return redirect('blocked')

    if request.method == "POST":
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            fs = FileSystemStorage()
            file_path = fs.save(excel_file.name, excel_file)
            file_full_path = fs.path(file_path)

            df = pd.read_excel(file_full_path)
            df = df[df.iloc[:, 0] != df.columns[0]]
            df.columns = ['Username', 'Password', 'Package']

            with open("generator/templates/generator/card_template.html", encoding="utf-8") as f:
                card_template = Template(f.read())

            cards = "\n".join([
                card_template.render(
                    username=row["Username"],
                    password=row["Password"],
                    package=row["Package"],
                    network_name=form.cleaned_data['network_name'],
                    login_page=form.cleaned_data['login_page'],
                    support_phone=form.cleaned_data['support_phone']
                ) for _, row in df.iterrows()
            ])

            full_html = Template(open("generator/templates/generator/page_template.html", encoding="utf-8").read()).render(cards_html=cards)

            if form.cleaned_data["format_choice"] == "pdf":
                pdf_path = os.path.join("media", "output.pdf")
                HTML(string=full_html).write_pdf(pdf_path)
                with open(pdf_path, "rb") as f:
                    response = HttpResponse(f.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
                    return response
            else:
                response = HttpResponse(full_html, content_type='text/html')
                response['Content-Disposition'] = 'attachment; filename="cards_output.html"'
                return response
    else:
        form = CardForm()
    return render(request, "generator/form.html", {"form": form})

@login_required
def blocked_view(request):
    return render(request, "generator/blocked.html")
