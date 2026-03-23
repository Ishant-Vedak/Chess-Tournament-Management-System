from django.core.management.commands import shell
from tournaments.models import Tournament, Participant, HostTournament, Round, Match

class Command(shell.BaseCommand):
    help='Function to add participants'

    def add_arguments(self, parser):
        parser.add_argument('tournament', type=str)
        parser.add_argument('number_of_participants', type=int)
        

    def handle(self, *args, **options):
        n = options['number_of_participants']
        t_name = options['tournament']
        try:
            t = Tournament.objects.get(name=t_name)
        except ValueError:
            raise ValueError('Provide a number value.')
        
        for i in range(1, n+1):
            Participant.objects.get_or_create(
                name = f'T{i}',
                tournament = t, 
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully made {n} participants.')
        )
        