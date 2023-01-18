from django.contrib import admin

from accounts.models import User, PhoneNumber


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "first_name", "last_name",
                    "date_joined", "last_login")


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")

admin.site.register(User, UserAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
# Register your models here.
