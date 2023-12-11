from django.core.management.base import BaseCommand

from base.listener import ResultListener

class Command(BaseCommand):
    print("Running listener")

    def handle(self, *args, **options):
        listener = ResultListener()
        listener.start()
        