import requests
import json
from datetime import datetime

from db import DBService


class Test:
    """Основной класс"""

    def __init__(self, x: int, y: int) -> None:
        self._validate_types(x, y, _type=int)
        self.x = x
        self.y = y
        self.db = DBService()

    def fetch_and_save_quizzes(self) -> None:
        """Получает список вопросов и сохраняет их в БД"""
        url = f'https://jservice.io/api/random?count={self.x}'
        response = requests.get(url)
        quizzes = response.json()

        self.db.save_quizzes(
            [(q['category']['title'], q['question'], q['answer']) for q in quizzes]
        )

    def get_category_count(self, category: str) -> int:
        """Возвращает количество записей в заданной категории"""
        self._validate_types(category, _type=str)
        return self.db.get_cat_count(category)

    def fetch_and_save_to_json(self) -> None:
        """Записывает случайные 'y' вопросов из БД в json-файл"""
        quizzes = self.db.fetch_records(self.y)

        current_date = datetime.now().strftime("%Y-%m-%d")
        json_filename = f'quizzes_{current_date}.json'

        with open(json_filename, 'w') as json_file:
            json.dump(quizzes, json_file)

    @staticmethod
    def _validate_types(*args, _type=None):
        """Валидирует аргументы по переданному типу"""
        if any(not isinstance(val, _type) for val in args):
            raise ValueError(f"Неверный тип аргумента")


if __name__ == "__main__":
    test_instance = Test(x=10, y=5)
    test_instance.fetch_and_save_quizzes()
    print(test_instance.get_category_count('names'))
    test_instance.fetch_and_save_to_json()
