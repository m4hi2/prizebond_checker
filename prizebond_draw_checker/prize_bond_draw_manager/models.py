import datetime
from typing import Dict, List, Type, TypeVar

import requests
from django.db import models
from dustu_lib.helpers import make_ordinal
from dustu_lib.models import TimeStampedUUIDModel

from .utils.prize_bond_pdf_parser import PrizeBondDrawParser

PR = TypeVar("PR", bound="PrizeBondDraw")
DW = TypeVar("DW", bound="DrawWinner")


class PrizeBondDraw(TimeStampedUUIDModel):
    """
    One:Many -> DrawWinner

    Data Held:
    1. Draw Term (draw_term)
    2. Draw Date (draw_date)
    3. Pointer to the  winning numbers (draw_winners)

    Responsibilities:
    1. Download a prize bond draw results
    2. Parse the draw results
    3. Create Winning number entries from the draw results
    """

    draw_term = models.IntegerField(blank=False, null=False, unique=True)
    draw_date = models.DateField(blank=True, null=True)

    def _download_prize_bond_draw_pdf(self) -> bytes | None:
        draw_term_ordinal = make_ordinal(self.draw_term)
        draw_pdf_url = f"https://www.bb.org.bd/investfacility/prizebond/{draw_term_ordinal}draw.pdf"

        pdf_response = requests.get(draw_pdf_url)

        # The page redirects to BB main site if the draw is not available
        if "<html>" in str(pdf_response.content):
            return None

        return pdf_response.content

    def _parse_draw_results(self, draw_pdf: bytes) -> Dict[str, List[str]]:
        parser = PrizeBondDrawParser(draw_pdf)

        return parser.parse_all_prize()

    def _create_draw_winners(self, all_prize: Dict[str, List[str]]):
        for prize_bracket, winning_numbers in all_prize.items():
            for winning_number in winning_numbers:
                DrawWinner.create(
                    winning_number=winning_number,
                    prize_bracket=prize_bracket,
                    draw=self,
                )

    def _set_draw_date(self) -> None:
        """The official draw date are the last day of the month every 3 months.
        But due to Bank holidays this draw date is sometimes not maintained.
        For the purpose of simplicity and since there is no easy way to get the
        actual dates of the draw, the draw dates are programmatically adjusted.
        """
        draw_date_80th = datetime.date(2015, 7, 31)

        draw_term_delta = self.draw_term - 80

        weeks_delta = draw_term_delta * 13  # 13 weeks is approx 3 months

        new_date = draw_date_80th + datetime.timedelta(weeks=weeks_delta)

        match new_date.month:
            case 12:
                new_date = datetime.date(new_date.year + 1, 1, 31)
            case 1:
                new_date = datetime.date(new_date.year, 1, 31)
            case 2:
                new_date = datetime.date(new_date.year, 1, 31)
            case 3:
                new_date = datetime.date(new_date.year, 4, 30)
            case 4:
                new_date = datetime.date(new_date.year, 4, 30)
            case 5:
                new_date = datetime.date(new_date.year, 4, 30)
            case 6:
                new_date = datetime.date(new_date.year, 7, 31)
            case 7:
                new_date = datetime.date(new_date.year, 7, 31)
            case 8:
                new_date = datetime.date(new_date.year, 7, 31)
            case 9:
                new_date = datetime.date(new_date.year, 10, 31)
            case 10:
                new_date = datetime.date(new_date.year, 10, 31)
            case 11:
                new_date = datetime.date(new_date.year, 10, 31)

        self.draw_date = new_date
        self.save()

    @classmethod
    def create(cls: Type[PR], draw_term: int) -> PR | None:
        instance: PrizeBondDraw = cls.objects.create(draw_term=draw_term)
        instance._set_draw_date()

        pdf = instance._download_prize_bond_draw_pdf()
        if not pdf:
            instance.delete()
            return None

        draw_results = instance._parse_draw_results(pdf)

        instance._create_draw_winners(draw_results)

        return instance

    @staticmethod
    def get_next_term() -> int:
        draw_terms: List[int] = [draw.draw_term for draw in PrizeBondDraw.objects.all()]

        next_term = max(draw_terms) + 1

        return next_term


class DrawWinner(TimeStampedUUIDModel):
    """
    Many:One -> PrizeBondDraw

    Data Held:
    1. Winning Number (winning_number)
    2. Prize Bracket (prize_bracket)
    3. Pointer to the draw of the winning number (draw)

    1. Keep track of the winning numbers and their prize brackets
    2. If needed point to the draw that the number belonged to
    3. Check if a number is a winning number
    """

    winning_number = models.CharField(max_length=7, null=False, blank=False)
    prize_bracket = models.CharField(max_length=6, null=False, blank=False)

    draw = models.ForeignKey(
        PrizeBondDraw, related_name="draw_winners", on_delete=models.CASCADE
    )

    @classmethod
    def create(
        cls: Type[DW], winning_number: str, prize_bracket: str, draw: PrizeBondDraw
    ) -> DW:
        instance = cls.objects.create(
            winning_number=winning_number, prize_bracket=prize_bracket, draw=draw
        )

        return instance

    @staticmethod
    def check_prize_bond_number(number: str) -> DW | None:
        try:
            winner: DrawWinner = DrawWinner.objects.get(winning_number=number)

            return winner
        except DrawWinner.DoesNotExist:
            return None
