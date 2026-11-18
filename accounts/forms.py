from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Vendor


class RegisterForm(UserCreationForm):
    business_name = forms.CharField(max_length=100, required=False)

    field_order = [
        "first_name", "last_name", "email", "contact_number",
        "role", "business_name", "password1", "password2",
    ]

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "contact_number", "role")
        widgets = {"role": forms.RadioSelect}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["role"].label = "I am registering as a"
        self.fields["business_name"].label = "Business name"
        self.fields["password1"].help_text = "At least 8 characters."
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("role") == User.Role.VENDOR:
            name = (cleaned.get("business_name") or "").strip()
            if not name:
                self.add_error("business_name", "Business name is required for vendors.")
            elif Vendor.objects.filter(business_name__iexact=name).exists():
                self.add_error("business_name", "This business name is already taken.")
            else:
                cleaned["business_name"] = name
        return cleaned

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and user.role == User.Role.VENDOR:
            Vendor.objects.create(
                user=user, business_name=self.cleaned_data["business_name"]
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "contact_number")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        taken = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if taken.exists():
            raise forms.ValidationError("This email is already used by another account.")
        return email


class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ("business_name", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}