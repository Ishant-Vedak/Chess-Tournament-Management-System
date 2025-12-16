from django.contrib import admin
from users.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    readonly_fields = ['is_staff', 'join_date']
    fieldsets = [
        (
            "Basic Info",
            {
                "fields": ['username', 'email', 'join_date', 'is_staff',]
            },
        ),
    ]