from pathlib import Path

import emails
from jinja2 import Template

from app.core.config import settings


def render_email_template(*, template_name: str, context: dict[str, any]):
    template_str = (
            Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()

    html_content = Template(template_str).render(context)
    return html_content


def send_email(email_to: str, subject: str, html_content):
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from="m.bychyniuk@gmail.com"
    )
    print(settings.SMTP_PASSWORD)
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT, "ssl": True,
                    "password": settings.SMTP_PASSWORD, "user": "m.bychyniuk@gmail.com"}
    response = message.send(to=email_to, smtp=smtp_options)
    print(response)


def generate_confirm_email(mail_to: str, username: str, confirm_token: str):
    link = settings.DOMAIN + settings.API_V1_STR + "/confirm-email?email=" + mail_to + "&token=" + confirm_token
    template = render_email_template(template_name="confirm_account.html",
                                     context={
                                         "username": username,
                                         "link": link
                                     })
    send_email(email_to=mail_to, subject="Confirming email.", html_content=template)
