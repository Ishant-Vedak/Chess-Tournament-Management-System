from django.core.management.commands import shell
from tournaments.models import Tournament, Participant, HostTournament, Round, Match

class Command(shell.BaseCommand):
    help='Function to reset tournament data easily.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        name = options['name']
        try: 
            t = Tournament.objects.get(name=name)
        except Tournament.DoesNotExist:
            raise NameError('Tournament Does Not Exist')

        HostTournament.objects.get(tournament=t).delete()
        Round.objects.filter(tournament=t).delete()
        for p in Participant.objects.filter(tournament=t).exclude(name='BYE'):
            p.points = 0
            p.save()
        t.is_finished = False
        t.save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully reset data for {name}.')
        )
        