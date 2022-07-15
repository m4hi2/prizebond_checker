import re

first_prize_pattern = re.compile(r"6,00,000/=\n \n([0-9]{6,7})\n", re.MULTILINE)
second_prize_pattern = re.compile(r"3,25,000/=\n \n([0-9]{6,7})\n", re.MULTILINE)
third_prize_pattern = re.compile(r"1,00,000/= UvKvi; †\n gvU 2wU\|\n \n\n([0-9]{6,7})\n \n([0-9]{6,7})\n", re.MULTILINE)
fourth_prize_pattern = re.compile(r"50,000/= UvKvi; †\n gvU 2wU\|\n \n\n([0-9]{6,7})\n \n([0-9]{6,7})\n", re.MULTILINE)
fifth_prize_pattern = re.compile(r"10,000/= UvKvi; \n†\ngvU 40wU\| \n([\n 0-9]*) \n\n \n   \n\n", re.MULTILINE)