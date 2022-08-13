from django.contrib.auth.models import User
from django.db import models


class PrizeDrawNumber(models.Model):
    prize_bond_number = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
