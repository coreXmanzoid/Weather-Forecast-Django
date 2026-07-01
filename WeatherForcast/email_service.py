import logging
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL

from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def send_link_email(user_email: str, reset_link: str, st: int) -> bool:
        """
        st = 1 -> Verify Email
        st = 2 -> Reset Password
        """

        if not EmailService.validate_email(user_email):
            logger.warning("Invalid email format: %s", user_email)
            return False

        sender_email = settings.EMAIL_HOST_USER
        sender_password = settings.EMAIL_HOST_PASSWORD
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        use_tls = settings.EMAIL_USE_TLS
        use_ssl = settings.EMAIL_USE_SSL
        timeout = getattr(settings, "EMAIL_TIMEOUT", 20)

        if not sender_email or not sender_password:
            logger.error(
                "Email configuration missing. "
                "Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py."
            )
            return False

        subject = (
            "Password Reset Link - ChatFlick"
            if st == 2
            else "Verify Email - ChatFlick"
        )

        button_text = "Reset Password" if st == 2 else "Verify Email"

        message_text = (
            "We received a request to reset your password."
            if st == 2
            else "Please verify your email address."
        )

        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = user_email
        msg["Subject"] = subject

        html_content = f"""
        <html>
            <body>
                <p>
                    Hello,<br><br>

                    {message_text} for <b>ChatFlick</b>.<br><br>

                    <a href="{reset_link}"
                       style="
                           display:inline-block;
                           background:#c7c0b1;
                           color:white;
                           padding:10px 20px;
                           border-radius:40px;
                           text-decoration:none;
                       ">
                        {button_text}
                    </a>

                    <br><br>

                    The link will expire in 20 minutes.<br>
                    If you did not request this, simply ignore this email.<br><br>

                    <b>ChatFlick Development Team</b>
                </p>
            </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        try:
            smtp_class = SMTP_SSL if use_ssl else SMTP

            with smtp_class(
                smtp_host,
                smtp_port,
                timeout=timeout,
            ) as connection:

                connection.ehlo()

                if use_tls and not use_ssl:
                    connection.starttls()
                    connection.ehlo()

                connection.login(sender_email, sender_password)
                connection.sendmail(
                    sender_email,
                    user_email,
                    msg.as_string(),
                )

            logger.info("Email sent successfully to %s", user_email)
            return True

        except Exception:
            logger.exception(
                "Failed to send email to %s using %s:%s (TLS=%s, SSL=%s)",
                user_email,
                smtp_host,
                smtp_port,
                use_tls,
                use_ssl,
            )
            return False