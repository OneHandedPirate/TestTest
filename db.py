import sqlite3


class DBService:
    """Вспомогательный класс для работы с базой данных"""

    def __init__(self) -> None:
        self._connection: sqlite3.Connection | None = None
        self._cursor: sqlite3.Cursor | None = None
        self._create_table()

    def __enter__(self) -> sqlite3.Cursor:
        self._connection = sqlite3.connect("quiz.db")
        self._cursor = self._connection.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._cursor.close()
        self._connection.close()

    def _create_table(self) -> None:
        """Создает таблицы 'quiz' и 'category' если они не существует"""
        with self as cursor:
            query1 = """
                    CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE
                    );
                    """
            query2 = """CREATE TABLE IF NOT EXISTS quiz (
                        id INTEGER PRIMARY KEY,
                        category_id INTEGER,
                        question TEXT,
                        answer TEXT,
                        FOREIGN KEY (category_id) REFERENCES category(id),
                        UNIQUE(question, answer)
                    );
                    """
            cursor.execute(query1)
            cursor.execute(query2)
            self._connection.commit()

    def _save_categories(self, categories: list[tuple]) -> None:
        """Сохраняет записи из списка 'categories' в базе данных, игнорируя дубликаты"""
        query = """INSERT OR IGNORE INTO category (name) VALUES (?)"""
        self._cursor.executemany(query, categories)
        self._connection.commit()

    def save_quizzes(self, quizzes: list[tuple]) -> None:
        """Сохраняет записи из списка 'quizzes'в базе данных, игнорируя дубликаты"""
        with self as cursor:
            categories = [(quiz[0],) for quiz in quizzes]
            self._save_categories(categories)

            query = """INSERT OR IGNORE INTO quiz (category_id, question, answer)
                    VALUES ((SELECT id FROM category WHERE name = ?), ?, ?)"""
            cursor.executemany(query, quizzes)
            self._connection.commit()

    def get_cat_count(self, category: str) -> int:
        """Возвращает количество записей в заданной категории"""
        with self as cursor:
            query = """SELECT COUNT(*) FROM category WHERE name = ?"""
            cursor.execute(query, (category,))
            return cursor.fetchone()[0]

    def fetch_records(self, num: int) -> list[dict]:
        """Возвращает случайно выбранные 'num' записей из базы данных"""
        with self as cursor:
            query = """SELECT c.name, q.question, q.answer  
                       FROM quiz q JOIN category c ON q.category_id = c.id
                       ORDER BY RANDOM() 
                       LIMIT ?"""
            cursor.execute(query, (num,))
            keys = ['category', 'question', 'answer']
            res = [{key: val for key, val in zip(keys, quiz)} for quiz in cursor.fetchall()]
            return res

