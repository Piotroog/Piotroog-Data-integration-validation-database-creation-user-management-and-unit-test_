import argparse
import sqlite3
import sys
import logging

class UserManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            sys.exit(1)

    def verify_credentials(self, login, password):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role FROM users WHERE (email = ? OR telephone_number = ?) "
            "AND password = ?",
            (login, login, password)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def print_all_accounts(self):
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(count)
        except sqlite3.Error as e:
            logging.error(f"Error querying the database: {e}")
        finally:
            conn.close()

    def print_oldest_account(self):
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT firstname, email, created_at FROM users "
                "ORDER BY created_at ASC LIMIT 1"
            )
            account = cursor.fetchone()
            if account:
                print(f"name: {account[0]}\nemail_address: {account[1]}"
                      f"\ncreated_at: {account[2]}")
        except sqlite3.Error as e:
            logging.error(f"Error querying the database: {e}")
        finally:
            conn.close()

    def group_by_age(self):
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT children FROM users")
            all_children = cursor.fetchall()

            age_count = {}
            for children in all_children:
                if children[0]:
                    for child in children[0].split(';'):
                        age = child.split()[1].strip('()')
                        if age.isdigit():
                            age_count[age] = age_count.get(age, 0) + 1

            for age, count in sorted(age_count.items(), key=lambda item: item[1]):
                print(f"age: {age}, count: {count}")
        except sqlite3.Error as e:
            logging.error(f"Error querying the database: {e}")
        finally:
            conn.close()

    def print_children(self, login):
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT children FROM users WHERE email = ? OR telephone_number = ?",
                (login, login)
            )
            children = cursor.fetchone()[0]
            if children:
                for child in sorted(children.split(';')):
                    print(child)
        except sqlite3.Error as e:
            logging.error(f"Error querying the database: {e}")
        finally:
            conn.close()

    def find_similar_children_by_age(self, login):
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT children FROM users WHERE email = ? OR telephone_number = ?",
                (login, login)
            )
            own_children_result = cursor.fetchone()
            own_children = own_children_result[0].split(';') if own_children_result and own_children_result[0] else []
            own_children_ages = {child.split()[1].strip('()') for child in own_children}

            cursor.execute(
                "SELECT firstname, telephone_number, children FROM users WHERE role = 'user'"
            )
            all_users = cursor.fetchall()

            for firstname, telephone, children_str in all_users:
                children = children_str.split(';') if children_str else []
                children_ages = {child.split()[1].strip('()') for child in children}
                common_ages = own_children_ages.intersection(children_ages)
                if common_ages:
                    children_info = '; '.join(
                        [child for child in children if child.split()[1].strip('()') in common_ages]
                    )
                    print(f"{firstname}, {telephone}: {children_info}")
        except sqlite3.Error as e:
            logging.error(f"Error querying the database: {e}")
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='User Management System')
    parser.add_argument('--login', required=True, help='User login - email or telephone number')
    parser.add_argument('--password', required=True, help='User password')
    parser.add_argument('--command', required=True, help='Command to execute')
    args = parser.parse_args()

    manager = UserManager('users_database.db')
    role = manager.verify_credentials(args.login, args.password)

    if role:
        if args.command == 'print-all-accounts' and role == 'admin':
            manager.print_all_accounts()
        elif args.command == 'print-oldest-account' and role == 'admin':
            manager.print_oldest_account()
        elif args.command == 'group-by-age' and role == 'admin':
            manager.group_by_age()
        elif args.command == 'print-children':
            manager.print_children(args.login)
        elif args.command == 'find-similar-children-by-age':
            manager.find_similar_children_by_age(args.login)
        else:
            print("Invalid command or insufficient permissions")
    else:
        print("Invalid Login")

if __name__ == "__main__":
    main()