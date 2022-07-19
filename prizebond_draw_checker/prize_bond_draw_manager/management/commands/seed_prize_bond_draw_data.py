from django.core.management.base import (BaseCommand, CommandError,
                                         CommandParser)
from django.db import IntegrityError

from ...models import PrizeBondDraw


class Command(BaseCommand):
    help = """
    Populates the database with data from 80th draw term upto the term provided
    as argument to this command
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--upto_term",
            type=int,
            help="Most recent term of prize bond draw, e.g. '107' for 107th draw",
        )

    def handle(self, *args, **options):
        if options["upto_term"]:
            upto_term = options["upto_term"]
        else:
            raise CommandError("--upto_term argument not provided.")

        for i in range(80, upto_term + 1):
            if i == 98:
                print("Term 98 is not parsable. Weird encoding...")
                continue
            try:
                PrizeBondDraw.create(i)
                print(f"Parsed Term: {i}")
            except IntegrityError:
                print(f"Term: {i} already exists.")
