import io
import re
from typing import Dict, List, Tuple

import PyPDF2

FIRST_PRIZE_PATTERN = re.compile(r"6,00,000/.*?([0-9]{6,7})", re.MULTILINE | re.DOTALL)
SECOND_PRIZE_PATTERN = re.compile(r"3,25,000/.*?([0-9]{6,7})", re.MULTILINE | re.DOTALL)
THIRD_PRIZE_PATTERN = re.compile(
    r"1,00,000/.*?(\d{6,7}).*?(\d{6,7})", re.MULTILINE | re.DOTALL
)
FOURTH_PRIZE_PATTERN = re.compile(
    r"50,000/.*?(\d{6,7}).*?(\d{6,7})", re.MULTILINE | re.DOTALL
)
FIFTH_PRIZE_PATTERN = re.compile(
    r"10,000/.*?([\n 0-9]{330,360})", re.MULTILINE | re.DOTALL
)


class PrizeBondDrawParser:
    """Prize bond draw result parser for 100th draw and onwards."""

    def __init__(self, prize_bond_draw_pdf_content_bytes: bytes) -> None:
        self.first_prize: List[str] = []
        self.second_prize: List[str] = []
        self.third_prize: List[str] = []
        self.fourth_prize: List[str] = []
        self.fifth_prize: List[str] = []

        prize_bond_draw_pdf_file_stream = io.BytesIO(prize_bond_draw_pdf_content_bytes)

        prize_bond_draw_pdf_reader = PyPDF2.PdfReader(prize_bond_draw_pdf_file_stream)
        prize_bond_draw_pdf_first_page = prize_bond_draw_pdf_reader.getPage(0)

        self.prize_bond_draw_pdf_text = prize_bond_draw_pdf_first_page.extract_text()

    @staticmethod
    def _populate_prize_brackets_with_cleaned_numbers(
        prize_bracket: List[str], prize_numbers: List[str] | Tuple[str]
    ) -> None:
        for number in prize_numbers:
            number = number.replace("\n", "")

            if len(number) < 4:
                continue

            if len(number) < 7:
                match len(number):
                    case 6:
                        number = "0" + number
                    case 5:
                        number = "00" + number
                    case 4:
                        number = "000" + number
            prize_bracket.append(number)

    def parse_first_prize(self) -> None:
        first_prize_numbers: List[str] = FIRST_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondDrawParser._populate_prize_brackets_with_cleaned_numbers(
            self.first_prize, first_prize_numbers
        )

    def parse_second_prize(self) -> None:
        second_prize_numbers: List[str] = SECOND_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        PrizeBondDrawParser._populate_prize_brackets_with_cleaned_numbers(
            self.second_prize, second_prize_numbers
        )

    def parse_third_prize(self) -> None:
        third_prize_numbers_list: List[Tuple[str]] = THIRD_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        third_prize_numbers = third_prize_numbers_list[0]

        PrizeBondDrawParser._populate_prize_brackets_with_cleaned_numbers(
            self.third_prize, third_prize_numbers
        )

    def parse_fourth_prize(self) -> None:
        fourth_prize_numbers_list: List[Tuple[str]] = FOURTH_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        fourth_prize_numbers = fourth_prize_numbers_list[0]

        PrizeBondDrawParser._populate_prize_brackets_with_cleaned_numbers(
            self.fourth_prize, fourth_prize_numbers
        )

    def parse_fifth_prize(self) -> None:
        fifth_prize_numbers_list: List[str] = FIFTH_PRIZE_PATTERN.findall(
            self.prize_bond_draw_pdf_text
        )

        fifth_prize_numbers_str = fifth_prize_numbers_list[0]
        fifth_prize_numbers_str = fifth_prize_numbers_str.strip()

        fifth_prize_numbers_combined = fifth_prize_numbers_str.split("\n")

        fifth_prize_numbers = []

        for combined_numbers in fifth_prize_numbers_combined:
            fifth_prize_numbers += combined_numbers.split()

        PrizeBondDrawParser._populate_prize_brackets_with_cleaned_numbers(
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
