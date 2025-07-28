from django.contrib import admin
from .models import Nashrie, Tags , Month , Year
# Register your models here.

admin.site.register(Tags)
admin.site.register(Nashrie)
admin.site.register(Month)
admin.site.register(Year)