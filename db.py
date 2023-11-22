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
        """Создает таблицу 'quiz', если она не существует"""
        with self as cursor:
            query = """
                    CREATE TABLE IF NOT EXISTS quiz (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    question TEXT,
                    answer TEXT,
                    UNIQUE(question, answer)
                    )
                    """
            cursor.execute(query)
            self._connection.commit()

    def save_quizzes(self, quizzes: list[tuple]) -> None:
        """Сохраняет записи из списка 'quizzes'в базе данных, игнорируя дубликаты"""
        with self as cursor:
            query = """INSERT OR IGNORE INTO quiz (category, question, answer)
                    VALUES (?, ?, ?)"""
            cursor.executemany(query, quizzes)
            self._connection.commit()

    def get_cat_count(self, category: str) -> int:
        """Возвращает количество записей в заданной категории"""
        with self as cursor:
            query = """SELECT COUNT(*) FROM quiz WHERE category = ?"""
            cursor.execute(query, (category,))
            return cursor.fetchone()[0]

    def fetch_records(self, num: int) -> list[tuple]:
        """Возвращает случайно выбранные 'num' записей из базы данных"""
        with self as cursor:
            query = """SELECT * FROM quiz ORDER BY RANDOM() LIMIT ?"""
            cursor.execute(query, (num,))
            return cursor.fetchall()

