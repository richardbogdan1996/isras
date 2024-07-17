import random
import string
import uuid

from main.models import User, Child
from datetime import datetime


def generate_user_code(request):
    while True:

        part1 = ''.join(random.choices(string.ascii_letters, k=2))
        part2 = ''.join(random.choices(string.digits, k=2))
        result_part1_part2 = part1 + part2
        part2 = datetime.now().strftime('%d%m%y')
        result = f"{result_part1_part2}-{part2}"

        if not User.objects.filter(user_code=result).exists():
            # Если код не существует, возвращаем его
            return result



def generate_test_code(reuest):
    while True:

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        part1 = ''.join(random.choice('0123456789') for _ in range(4))
        part2 = f"{current_day:02d}{current_month:02d}"
        current_year = str(current_year)
        part3 = current_year[-2:]
        result_part = ''.join([part2, part3])
        result_test_code = f"{part1}{result_part}"

        if not Child.objects.filter(child_code=result_test_code).exists():
            return result_test_code




def generate_child_code(request):
    while True:

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day

        part1 = ''.join(random.choices(string.ascii_letters, k=2))
        part2 = ''.join(random.choices(string.digits, k=2))
        result_part1_part2 = part1 + part2
        part2 = datetime.now().strftime('%d%m%y')
        result = f"{result_part1_part2}-{part2}"


        # Проверяем, существует ли сгенерированный код в базе данных
        if not Child.objects.filter(child_code=result).exists():
            # Если код не существует, возвращаем его
            return result