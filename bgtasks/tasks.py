import smtplib
import sqlite3

from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT


def get_email():
    with sqlite3.connect(database="C:\\Users\\user\\PycharmProjects\\fastAPI-code\\models\\database.db") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT email FROM user
                WHERE id = (SELECT MAX(id) FROM user);
                """
            )
            email = cursor.fetchall()
            return email[0][0]
        except Exception as ex:
            return f"Something wrong\n{ex}"


def get_account(account_id: int = 1):
    with sqlite3.connect(database="C:\\Users\\user\\PycharmProjects\\fastAPI-code\\models\\database.db") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                SELECT data FROM account_sell JOIN account ON account_id = id
                WHERE id = {account_id};
                """
            )
            account = cursor.fetchall()
            return account[0][0]
        except Exception as ex:
            return f"Something wrong\n{ex}"


def send_message(customer_email: str, account_id: int, ) -> str:
    sender = SMTP_USER
    password = SMTP_PASSWORD
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    try:
        server.login(sender, password)
        text_msg = "Thanks for buying! Your account: "
        account_data = get_account(account_id)
        server.sendmail(sender, customer_email, f"Subject: Your account!\n{text_msg}\n{account_data}")
        return "success"
    except Exception as _ex:
        return f"error: {_ex}\nCheck email or pass"


if __name__ == "__main__":
    print(send_message(get_email(), 1))
    print(get_email())
    print(get_account())
