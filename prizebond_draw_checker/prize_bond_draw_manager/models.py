from typing import Dict, List

import requests
from django.db import models
from dustu_lib.helpers import make_ordinal
from dustu_lib.models import TimeStampedUUIDModel

from .utils.prize_bond_pdf_parser import PrizeBondDrawParser


class PrizeBondDraw(TimeStampedUUIDModel):
    draw_term = models.IntegerField(blank=False, null=False)
    draw_date = models.DateField(blank=True, null=True)

    @classmethod
    def create(cls, draw_term: int):
        instance = cls.objects.create(draw_term=draw_term)

        return instance

    def _download_prize_bond_draw_pdf(self) -> bytes:
        draw_term_ordinal = make_ordinal(self.draw_term)
        draw_pdf_url = f"https://www.bb.org.bd/investfacility/prizebond/{draw_term_ordinal}draw.pdf"

        pdf_response = requests.get(draw_pdf_url)

        return pdf_response.content

    def _parse_draw_results(self, draw_pdf: bytes) -> Dict[str, List[str]]:
        parser = PrizeBondDrawParser(draw_pdf)

        return parser.parse_all_prize()


class DrawWinner(TimeStampedUUIDModel):
    winning_number = models.CharField(max_length=7, null=False, blank=False)
    prize_bracket = models.CharField(max_length=6, null=False, blank=False)

    draw = models.ForeignKey(
        PrizeBondDraw, related_name="draw_winners", on_delete=models.CASCADE
    )
