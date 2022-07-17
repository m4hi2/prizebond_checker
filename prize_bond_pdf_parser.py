import io
import re

import PyPDF2

first_prize_pattern = re.compile(r"6,00,000/=\n \n([0-9]{6,7})\n", re.MULTILINE)
second_prize_pattern = re.compile(r"3,25,000/=\n \n([0-9]{6,7})\n", re.MULTILINE)
third_prize_pattern = re.compile(
    r"1,00,000/=.*([0-9]{6,7})\n \n([0-9]{6,7})\n", re.MULTILINE | re.DOTALL
)
fourth_prize_pattern = re.compile(
    r"50,000/=.*?\n([0-9]{6,7})\n \n([0-9]{6,7})\n", re.MULTILINE | re.DOTALL
)
fifth_prize_pattern = re.compile(r"10,000/=.*?([\n 0-9]*)\[", re.MULTILINE | re.DOTALL)
