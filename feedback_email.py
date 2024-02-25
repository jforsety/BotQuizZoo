import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL, EMAIL_PASSWORD
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования

# настроим rfl
handler = RotatingFileHandler('Logs/LogsFeedback.log', maxBytes=5000000, backupCount=5, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)


def send_email(message):
    sender = EMAIL # Email
    password = EMAIL_PASSWORD # Пароль от приложения, если используем яндекс.
    server = smtplib.SMTP("smtp.yandex.ru", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEMultipart()

        msg["Subject"] = "Обратная связь"
        with open("Feedback/feedback.txt", encoding='utf-8') as f:
            file = MIMEText(f.read())
        file.add_header('content-disposition', 'attachment', filename="feedback.txt")
        msg.attach(file)
        server.sendmail(sender, sender, msg.as_string())
        logger.info("Письмо с обратной связью отправлено")
        return "Письмо с обратной связью отправлено"
    except Exception as _ex:
        logger.info("Письмо с обратной связью отправлено")
        return f'{_ex} Письмо не отправлено'


def main():
    message = "Письмо с обратной связью от пользователя"
    print(send_email(message=message))


if __name__ == "__main__":
    main()