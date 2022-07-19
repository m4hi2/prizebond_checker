import requests
from django.db import models
from dustu_lib.models import TimeStampedUUIDModel


class PrizeBondDraw(TimeStampedUUIDModel):
    draw_term = models.IntegerField(blank=False, null=False)
    draw_date = models.DateField(blank=True, null=True)

    @classmethod
    def create(cls, draw_term: int):
        cls.objects.create(draw_term=draw_term)


class DrawWinner(TimeStampedUUIDModel):
    winning_number = models.CharField(max_length=7, null=False, blank=False)
    prize_bracket = models.CharField(max_length=6, null=False, blank=False)

    draw = models.ForeignKey(
        PrizeBondDraw, related_name="draw_winners", on_delete=models.CASCADE
    )
