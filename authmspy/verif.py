import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

SMTP_CONFIG={
    "server": config.settings.smtp_host ,
    "port": config.settings.smtp_port,
    "username": config.settings.smtp_user,
    "password": config.settings.smtp_password
}

def send_confirmation_code(email,code):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_CONFIG['username']
        msg['To'] = email
        msg['Subject'] = "Код подтверждения регистрации"
        
        body = f"""
        <h2>Добро пожаловать!</h2>
        <p>Ваш код подтверждения: <strong>{code}</strong></p>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port']) as server:
            server.starttls()
            server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
            server.send_message(msg)
        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False
