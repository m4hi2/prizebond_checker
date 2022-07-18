import io
import re
from typing import Dict, List

import PyPDF2

FIRST_PRIZE_PATTERN = re.compile(r"6,00,000/=\n \n([0-9]{6,7})\n", re.MULTILINE)
SECOND_PRIZE_PATTERN = re.compile(r"3,25,000/=\n \n([0-9]{6,7})\n", re.MULTILINE)
THIRD_PRIZE_PATTERN = re.compile(
    r"1,00,000/=.*?([0-9]{6,7}\n \n[0-9]{6,7})\n", re.MULTILINE | re.DOTALL
)
FOURTH_PRIZE_PATTERN = re.compile(
    r"50,000/=.*?\n([0-9]{6,7}\n \n[0-9]{6,7})\n", re.MULTILINE | re.DOTALL
)
FIFTH_PRIZE_PATTERN = re.compile(r"10,000/=.*?([\n 0-9]*)\[", re.MULTILINE | re.DOTALL)


class PrizeBondParser:
    first_prize: List[str] = []
    second_prize: List[str] = []
    third_prize: List[str] = []
    fourth_prize: List[str] = []
    fifth_prize: List[str] = []

    def __init__(self, prize_bond_draw_pdf_content_bytes: bytes) -> None:
        prize_bond_draw_pdf_file_stream = io.BytesIO(prize_bond_draw_pdf_content_bytes)

        prize_bond_draw_pdf_reader = PyPDF2.PdfReader(prize_bond_draw_pdf_file_stream)
        prize_bond_draw_pdf_first_page = prize_bond_draw_pdf_reader.getPage(0)

        self.prize_bond_draw_pdf_text = prize_bond_draw_pdf_first_page.extract_text()

    @staticmethod
    def _populate_prize_brackets_with_cleaned_numbers(
        prize_bracket: List[str], prize_numbers: List[str]
    ) -> None:
        numbers = prize_numbers[0].replace("\n", "")
        numbers = numbers.strip()

        for number in numbers.split():
            if len(number) < 7:
                match len(number):
                    case 6:
                        number = "0" + number
                    case 5:
                        number = "00" + number

            prize_bracket.append(number)

    def parse_first_prize(self) -> None:
        first_prize_numbers: List[str] = FIRST_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondParser._populate_prize_brackets_with_cleaned_numbers(
            self.first_prize, first_prize_numbers
        )

    def parse_second_prize(self) -> None:
        second_prize_numbers: List[str] = SECOND_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondParser._populate_prize_brackets_with_cleaned_numbers(
            self.second_prize, second_prize_numbers
        )

    def parse_third_prize(self) -> None:
        third_prize_numbers: List[str] = THIRD_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondParser._populate_prize_brackets_with_cleaned_numbers(
            self.third_prize, third_prize_numbers
        )

    def parse_fourth_prize(self) -> None:
        fourth_prize_numbers: List[str] = FOURTH_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondParser._populate_prize_brackets_with_cleaned_numbers(
            self.fourth_prize, fourth_prize_numbers
        )

    def parse_fifth_prize(self) -> None:
        fifth_prize_numbers: List[str] = FIFTH_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondParser._populate_prize_brackets_with_cleaned_numbers(
            self.fifth_prize, fifth_prize_numbers
        )

    def parse_all_prize(self) -> Dict[str, List[str]]:
        self.parse_first_prize()
        self.parse_second_prize()
        self.parse_third_prize()
        self.parse_fourth_prize()
        self.parse_fifth_prize()

        all_prize_numbers = {
            "first_prize": self.first_prize,
            "second_prize": self.second_prize,
            "third_prize": self.third_prize,
            "fourth_prize": self.fourth_prize,
            "fifth_prize": self.fifth_prize,
        }

        return all_prize_numbers
