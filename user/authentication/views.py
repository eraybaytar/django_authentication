from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import User
from .decorators import role_required
from .forms import RegisterForm, LoginForm, PasswordResetRequestForm, SetNewPasswordForm

# Create your views here.

def dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(id=user_id)
    return HttpResponse(f"Hoş geldin {user.full_name} - Rolün: {user.role}")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return HttpResponse("Email zaten kayıtlı.", status=400)
            user = User(
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name']
            )
            user.set_password(form.cleaned_data['password'])
            token = user.generate_token("email_verification_token")
            user.save()
            return HttpResponse("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                if user.check_password(form.cleaned_data['password']):
                    request.session['user_id'] = user.id
                    return redirect("dashboard")
                return HttpResponse("Hatalı şifre!", status=401)
            except User.DoesNotExist:
                return HttpResponse("Kullanıcı bulunamadı", status=404)
    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})

def logout_view(request):
    request.session.flush()
    return redirect("login")

def reset_password_request_view(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data["email"])
                token = user.generate_token("reset_password_token")
                reset_url = request.build_absolute_uri(
                    reverse("reset_password") + f"?token={token}"
                )
                print(f"[KONSOLDA ŞİFRE SIFIRLAMA LİNKİ]: {reset_url}")
                messages.success(request, "Eğer e-posta sistemde varsa, bir bağlantı gönderildi.")
            except User.DoesNotExist:
                # Gizli tutmak için her durumda aynı mesajı veriyoruz
                messages.success(request, "Eğer e-posta sistemde varsa, bir bağlantı gönderildi.")
            return redirect("login")
    else:
        form = PasswordResetRequestForm()
    return render(request, "authentication/reset_request.html", {"form": form})


def reset_password_view(request):
    token = request.GET.get("token", "")
    try:
        user = User.objects.get(reset_password_token=token)
    except User.DoesNotExist:
        return HttpResponse("Geçersiz veya süresi dolmuş bağlantı.", status=400)

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password"])
            user.reset_password_token = None  # Token'ı geçersiz kıl
            user.save()
            messages.success(request, "Şifreniz başarıyla güncellendi.")
            return redirect("login")
    else:
        form = SetNewPasswordForm()
    return render(request, "authentication/reset_password.html", {"form": form})

@role_required(['admin'])
def admin_dashboard_view(request):
    return render(request, 'accounts/admin_dashboard.html')
