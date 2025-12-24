from django.contrib import admin
from clubs.models import Club, ClubMembership

# Register your models here.

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'website')
    readonly_fields = ['creation_date']
    fieldsets = [
        (
            "Basic Info",
            {
                "fields": ['name', 'creation_date', 'website',]
            },
        ),
    ]   

admin.site.register(ClubMembership)