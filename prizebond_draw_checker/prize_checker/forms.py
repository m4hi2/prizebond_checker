from typing import List

from django import forms

from prize_bond_draw_manager.utils.prize_bond_pdf_parser import PrizeBondDrawParser


class PrizeBondNumberForm(forms.Form):
    prize_bond_numbers = forms.CharField(label="Prize Bond Numbers", max_length=100)

    def get_numbers(self):
        if self.is_valid():
            prize_bond_numbers = self.cleaned_data["prize_bond_numbers"]
            for char in prize_bond_numbers:
                if not PrizeBondNumberForm.validate_char(char):
                    print("gg")
                    raise forms.ValidationError(f"'{char}' is not allowed in the form.")

            return PrizeBondNumberForm._get_numbers(prize_bond_numbers)

    @staticmethod
    def validate_char(char: str) -> bool:
        allowed_chars = "1234567890,~ "
        if char in allowed_chars:
            return True
        return False

    @staticmethod
    def _get_numbers(numbers_string: str) -> List[str]:
        numbers_group = numbers_string.split(",")
        numbers_group = [number_group.strip() for number_group in numbers_group]

        numbers_cleaned = []
        for numbers in numbers_group:
            if "~" in numbers:
                number_low, number_high = [int(number.strip()) for number in numbers.split("~")]
                for number in range(number_low, number_high + 1):
                    number_str = str(number)
                    number = PrizeBondDrawParser.fix_number_size(number_str)
                    numbers_cleaned.append(number)

            if len(numbers) == 7:
                numbers_cleaned.append(numbers)
            else:
                raise forms.ValidationError(f"{numbers} is not valid because, length of the number is not 7 digits.")

        return numbers_cleaned
