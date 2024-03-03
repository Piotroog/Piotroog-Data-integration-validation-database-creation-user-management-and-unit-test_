import unittest
from user_manager import UserManager

class TestUserManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = UserManager('test_database.db')
        cls.setup_test_database()

    @classmethod
    def setup_test_database(cls):
        conn = cls.manager.create_connection()
        cursor = conn.cursor()

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS users ('
            'id INTEGER PRIMARY KEY, '
            'email TEXT NOT NULL, '
            'telephone_number TEXT, '
            'password TEXT NOT NULL, '
            'role TEXT NOT NULL, '
            'created_at TEXT NOT NULL, '
            'children TEXT, '
            'firstname TEXT)'
        )

        cursor.execute(
            "INSERT INTO users (email, telephone_number, password, role, "
            "created_at, children, firstname) VALUES "
            "('test_email@example.com', '123456789', 'test_password', 'admin', "
            "'2020-01-01 00:00:00', 'Child1 (10); Child2 (5)', 'Test User')"
        )

        conn.commit()
        conn.close()

    def test_verify_credentials(self):
        result = self.manager.verify_credentials('test_email@example.com', 'test_password')
        self.assertIsNotNone(result)

    def test_print_all_accounts(self):
        self.manager.print_all_accounts()

    def test_print_oldest_account(self):
        self.manager.print_oldest_account()

    def test_group_by_age(self):
        self.manager.group_by_age()

    def test_print_children(self):
        self.manager.print_children('test_email@example.com')

    def test_find_similar_children_by_age(self):
        self.manager.find_similar_children_by_age('test_email@example.com')

if __name__ == '__main__':
    unittest.main()