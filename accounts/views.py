from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .decorators import role_required
from .forms import RegisterForm, UserProfileForm, VendorProfileForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("login")
        messages.error(request, "Please fix the errors below.")
    return render(request, "accounts/register.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def dashboard(request):
    """Sends each user to the dashboard for their role."""
    if request.user.role == User.Role.VENDOR:
        return redirect("vendor_dashboard")
    return redirect("customer_dashboard")


@role_required(User.Role.CUSTOMER)
def customer_dashboard(request):
    return render(request, "accounts/customer_dashboard.html")


@role_required(User.Role.VENDOR)
def vendor_dashboard(request):
    return render(request, "accounts/vendor_dashboard.html")


@login_required
def profile(request):
    vendor = getattr(request.user, "vendor", None)
    return render(request, "accounts/profile.html", {"vendor": vendor})


@login_required
def profile_edit(request):
    # Always uses request.user, so users can only edit their own profile.
    vendor = getattr(request.user, "vendor", None)
    user_form = UserProfileForm(request.POST or None, instance=request.user)
    vendor_form = (
        VendorProfileForm(request.POST or None, instance=vendor) if vendor else None
    )

    if request.method == "POST":
        valid = user_form.is_valid() and (vendor_form is None or vendor_form.is_valid())
        if valid:
            user_form.save()
            if vendor_form:
                vendor_form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
        messages.error(request, "Please fix the errors below.")

    return render(
        request,
        "accounts/profile_edit.html",
        {"user_form": user_form, "vendor_form": vendor_form},
    )