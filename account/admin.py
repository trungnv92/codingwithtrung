from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ['phone','email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff']
    search_fields = ['phone','email', 'username']
    readonly_fields = ['date_joined', 'last_login']
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)