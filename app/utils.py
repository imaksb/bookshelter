from pathlib import Path

import emails
from jinja2 import Template


def render_email_template(*, template_name: str, context: dict[str, any]):
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()

    html_content = Template(template_str).render(context)
    return html_content


def send_email(email: str, subject: str, message: str):
    pass
