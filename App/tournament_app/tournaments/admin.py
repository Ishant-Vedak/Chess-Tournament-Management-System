from django.contrib import admin
from tournaments.models import Tournament, JoinTournament

# Register your models here.

class JoinTournamentInline(admin.TabularInline):
    model = Tournament.participants.through
    extra = 1

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "type")
    list_filter = ("status",)
    search_fields = ("name",)
    ordering = ("-creation_date",)
    readonly_fields = ["creation_date"]

    fieldsets = [
        (
            'Basic Info',
            {
                "fields": ["name", "lead_organizer", "club", "creation_date", "status", "type",]
            },
        ),
    ]

    inlines = [
        JoinTournamentInline
    ]
    exclude = [
        'participants'
    ]


admin.site.register(JoinTournament)