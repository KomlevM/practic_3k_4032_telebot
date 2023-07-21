import os
import telebot
import shutil
import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



def send_email(folder_path):
    
    smtp_server = 'smtp.mail.ru'  
    smtp_port = 465  
    sender_email = 'komlevmaxi@mail.ru'
    receiver_email = 'komlev.maxim2002@mail.ru'
    sender_password = 'Qy4xtMHGxp13DNZzX8de'
    subject = 'Клиент с бота'
    
    # Создание объекта MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Получение списка файлов в папке
    files = os.listdir(folder_path)

    # Прикрепление файлов к письму
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        attachment = open(file_path, 'rb')

        # Создание объекта MIMEBase
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())

        # Кодирование вложения в base64
        encoders.encode_base64(mime_base)

        # Добавление заголовка
        mime_base.add_header('Content-Disposition', f'attachment; filename= {file_name}')

        # Прикрепление вложения к письму
        msg.attach(mime_base)
        attachment.close()

    # Отправка письма
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Письмо успешно отправлено!")

        shutil.rmtree(folder_path)  # исправлено на `os.remove` для удаления файла, а не папки
    except Exception as e:
        print("Ошибка при отправке письма:", str(e))