from typing import Dict, List, Type, TypeVar

import requests
from django.db import models
from dustu_lib.helpers import make_ordinal
from dustu_lib.models import TimeStampedUUIDModel

from .utils.prize_bond_pdf_parser import PrizeBondDrawParser

PR = TypeVar("PR", bound="PrizeBondDraw")
DW = TypeVar("DW", bound="DrawWinner")


class PrizeBondDraw(TimeStampedUUIDModel):
    draw_term = models.IntegerField(blank=False, null=False)
    draw_date = models.DateField(blank=True, null=True)

    @classmethod
    def create(cls: Type[PR], draw_term: int) -> PR:
        instance: PrizeBondDraw = cls.objects.create(draw_term=draw_term)

        pdf = instance._download_prize_bond_draw_pdf()
        draw_results = instance._parse_draw_results(pdf)

        instance._create_draw_winners(draw_results)

        return instance

    def _download_prize_bond_draw_pdf(self) -> bytes:
        draw_term_ordinal = make_ordinal(self.draw_term)
        draw_pdf_url = f"https://www.bb.org.bd/investfacility/prizebond/{draw_term_ordinal}draw.pdf"

        pdf_response = requests.get(draw_pdf_url)

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


class DrawWinner(TimeStampedUUIDModel):
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
