from django.contrib import admin
from Users.models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['date_joined', 'is_staff', 'is_active']


admin.site.register(CustomUser, CustomUserAdmin)