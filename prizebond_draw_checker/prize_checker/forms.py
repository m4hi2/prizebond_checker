from django import forms


class PrizeBondNumberForm(forms.Form):
    prize_bond_numbers = forms.CharField(label="Prize Bond Numbers", max_length=100)
