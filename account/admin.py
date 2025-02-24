from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, ProfileIcon
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("first_name", "last_name","email","is_active",)
    list_filter = ("email",  "is_active",'gender')
    ordering = ("first_name",)
    search_fields = ("email",'first_name')

    fieldsets = (
        (None, {"fields": ("password","email")}),
        ("Info", {"fields": ("first_name", "last_name", "mobile_number","gender",'id_number','selected_icon')}),
        ("Accounts", {"fields": ("main_balance", "revenue_share")}),
        ("Permissions", {"fields": ('max_clan_create','max_clans_joined',"is_staff", "is_active")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name","last_name",'id_number','mobile_number',"password1", "password2",
                "is_active"
            )}
        ),
    )
    


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(ProfileIcon)