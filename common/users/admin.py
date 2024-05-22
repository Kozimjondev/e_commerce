from django.conf import settings
from django.contrib import admin
from django.contrib.auth import hashers
from django.contrib.auth.decorators import login_required
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    exclude = ["created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        # Hash the password before saving the object
        if obj.password:
            obj.password = hashers.make_password(password=obj.password)
        super().save_model(request, obj, form, change)

