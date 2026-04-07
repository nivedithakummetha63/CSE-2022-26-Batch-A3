from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from base.models import Profile
from .emails import account_activation_email
import uuid
def login_view(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin/')
                next_url = request.GET.get("next")
                return redirect(next_url if next_url else "/app/")
            else:
                messages.error(request, "Please verify your email before logging in.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# -----------------------------------
# REGISTER VIEW (EMAIL VERIFICATION)
# -----------------------------------
def register(request):
    # Logout any currently authenticated user (including admin)
    if request.user.is_authenticated:
        logout(request)
    
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")


        # create user (inactive)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
        )

        # create profile with email token
        email_token = uuid.uuid4()
        Profile.objects.create(
            user=user,
            email_token=email_token,
            is_verified=False
        )

        # send activation email (wrapped to prevent crash if email fails)
        try:
            account_activation_email(email, str(email_token))
            messages.success(
                request,
                "Account created successfully. Please check your email to activate your account."
            )
        except Exception:
            messages.success(
                request,
                "Account created successfully. If you don't receive an email, contact support."
            )
        return redirect("login")

    return render(request, "accounts/register.html")


# -----------------------------------
# ACCOUNT ACTIVATION
# -----------------------------------
def activate_account(request):
    token = request.GET.get("token")

    if not token:
        messages.error(request, "Invalid activation link.")
        return redirect("login")

    try:
        # Convert string token to UUID
        token_uuid = uuid.UUID(token)
        profile = Profile.objects.get(email_token=token_uuid)

        if profile.is_verified:
            messages.info(request, "Account already activated.")
            return redirect("login")

        profile.is_verified = True
        profile.save()

        user = profile.user
        user.is_active = True
        user.save()

        messages.success(request, "Account activated successfully. Please login.")
        return redirect("login")

    except (Profile.DoesNotExist, ValueError):
        messages.error(request, "Invalid or expired activation link.")
        return redirect("login")


# -----------------------------------
# LOGOUT
# -----------------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("/")
