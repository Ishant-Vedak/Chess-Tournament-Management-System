from django.contrib import admin
from clubs.models import Club, ClubMembership

# Register your models here.
class ClubMembershipInline(admin.TabularInline):
    model = Club.members.through
    extra = 1


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
    inlines = [
        ClubMembershipInline,
    ]
    exclude = [
        "members"
    ]




admin.site.register(ClubMembership)