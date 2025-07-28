from distutils.command.register import register
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

from .forms import CustomChangeForm , CustomCreationForm

from .models import CustomUser ,  Category

# Register your models here.

class CustomAdmin(UserAdmin):
    class Meta:
        model = CustomUser
        add_form = CustomCreationForm
        form = CustomChangeForm
        list_display = ['username' , 'email' , 'phone_number' , 'roles']
        fieldsets = UserAdmin.fieldsets + (
            (None , {'fields':('phone_number' ,'image' , 'roles')}),
        )
        add_fieldsets = UserAdmin.add_fieldsets + (
            (None , {'fields':('phone_number' , 'image' , 'roles')}),
        )

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username','password','phone_number', 'image', 'roles','category' , 'img_accept')})
UserAdmin.fieldsets = tuple(fields)


admin.site.register(CustomUser ,UserAdmin)


admin.site.register(Category)

# class AccountInline (admin.StackedInline):
#     model = CustomUser



# admin.site.register(CustomUser , CustomAdmin)



# class CustomAdmin(UserAdmin):
#     add_form = CustomCreationUser
#     form = CustomChangeUser
#     model = CustomUser
#     list_display = ['username' , 'email' , 'age' , 'is_staff']
#     fieldsets = UserAdmin.fieldsets + (
#         (None , {'fields':('age' ,)}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None , {'fields':('age' ,)}),
#     )


# admin.site.register(CustomUser , CustomAdmin)