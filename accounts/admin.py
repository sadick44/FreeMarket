from django.contrib import admin

from accounts.models import User, PhoneNumber, Post, Image


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "first_name", "last_name",
                    "date_joined", "last_login")

class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")


class PostAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")


class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'images']


admin.site.register(User, UserAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
# Register your models here.
