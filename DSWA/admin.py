from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, ConfidentialData, AuditLog


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'date_of_birth', 'is_verified')
#     list_filter = ('is_staff', 'is_superuser', 'is_active')
#     search_fields = ('username', 'email')
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'last_name', 'first_name', 'date_of_birth', 'gender', 'is_verified','encryption_key']





@admin.register(ConfidentialData)
class ConfidentialDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'is_encrypted', 'encryption_key')
    list_filter = ('is_encrypted',)
    search_fields = ('user__username', 'user__email')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'action', 'ip_address', 'success')
    list_filter = ('action', 'success')
    search_fields = ('user__username', 'user__email', 'ip_address')
