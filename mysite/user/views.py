from django.shortcuts import render
from django.contrib import messages
from user.forms import SignupForm, LoginForm, ChangePasswordForm, ProfileUpdateForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from user.email import send_email_verification
from django.contrib.auth import get_user_model
from user.utils import EmailVerificationTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


User = get_user_model()

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully! Please Login")
            return HttpResponseRedirect(reverse("index"))
        messages.error(request, "Please enter valid data")
        return render(request, "user/signup.html", {"form": form})
    # Get Request
    context = {
        "form": SignupForm()
    }
    return render(request, "user/signup.html", context)

def login(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                user_login(request, user)
                messages.success(request, "Logged in successfully")
                return HttpResponseRedirect(reverse("index"))
            messages.error(request, "Please enter valid credentials")
            return HttpResponseRedirect(reverse("user:login"))
        messages.error(request, "Please enter valid credentials")
        return HttpResponseRedirect(reverse("user:login"))
    # GET 
    context = {
        "form": LoginForm()
    }
    return render(request, "user/login.html", context)


def logout(request):
    user_logout(request)
    messages.info(request, "Logged out successfully")
    return HttpResponseRedirect(reverse("user:login"))

def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully")
            return HttpResponseRedirect(reverse("index"))
        messages.error(request, "Please enter valid data")
        return render(request, "user/change-password.html", {"form": form})
    # GET
    context = {
        "form": ChangePasswordForm(request.user)
    }
    return render(request, "user/change-password.html", context)

def profile_view(request):
    context = {
        "user": request.user
    }
    return render(request, "user/profile-view.html", context)

def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return HttpResponseRedirect(reverse("user:profile-view"))
        messages.error(request, "Please enter valid data")
        return render(request, "user/profile-update.html", {"form": form})
    # GET request
    context = {
        "form": ProfileUpdateForm(instance=request.user)
    }
    return render(request, "user/profile-update.html", context)

def email_verificatin_request(request):
    if not request.user.is_email_verified:
        send_email_verification(request, request.user.id)
        return HttpResponse("Email Verification Link sent to your email address")
    return HttpResponseForbidden("Email already verified")

def email_verifier(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None
    

    if user == request.user:
        if EmailVerificationTokenGenerator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            messages.success(request, "Email address verified")
            return HttpResponseRedirect(reverse("user:profile-view"))
        return HttpResponseBadRequest("Invalid request")
    return HttpResponseForbidden("You dont have permission to use this link")