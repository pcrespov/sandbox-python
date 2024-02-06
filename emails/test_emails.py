# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

#
# SEE https://docs.python.org/3/library/email.examples.html
# SEE https://jinja.palletsprojects.com/en/3.0.x/api/#basics
#
#


import base64
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

from faker import Faker
from jinja2 import DictLoader, Environment, select_autoescape


def compose_branded_email(
    msg: EmailMessage, text_body, html_body, attachments: list[Path]
) -> EmailMessage:
    # Text version
    msg.set_content(
        f"""\
        {text_body}

        Done with love at Z43
    """
    )

    # HTML version
    logo_path = Path(
        "services/static-webserver/client/source/resource/osparc/z43-logo.png"
    )

    encoded = base64.b64encode(logo_path.read_bytes()).decode()
    img_src_as_base64 = f'"data:image/jpg;base64,{encoded}">'
    assert img_src_as_base64

    # Adding an image as CID attachments (which get embedded with a MIME object)
    logo_cid = make_msgid()
    img_src_as_cid_atttachment = f'"cid:{logo_cid[1:-1]}"'

    img_src = img_src_as_cid_atttachment
    msg.add_alternative(
        f"""\
    <html>
    <head></head>
    <body>
        {html_body}
        Done with love at <img src={img_src} width=30/>
    </body>
    </html>
    """,
        subtype="html",
    )

    assert msg.is_multipart()

    maintype, subtype = _guess_file_type(logo_path)
    msg.get_payload(1).add_related(
        logo_path.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        cid=logo_cid,
    )

    # Attach files
    _add_attachments(msg, attachments)
    return msg


def create_user_email(osparc_simcore_root_dir):
    # this is the new way to cmpose emails
    msg = EmailMessage()
    msg["From"] = Address(display_name="osparc support", addr_spec="support@osparc.io")
    msg["Subject"] = "Payment invoice"
    text_body = """\
    Hi there,

    This is your invoice.
    """

    html_body = """\
    <p>Hi there!</p>
    <p>This is your
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            invoice
        </a>.
    </p>
    """
    msg = compose_branded_email(
        msg, text_body, html_body, attachments=[osparc_simcore_root_dir / "ignore.pdf"]
    )


async def test_it(
    tmp_path: Path,
    faker: Faker,
):
    settings = SMTPSettings.create_from_envs()
    env = Environment(
        loader=DictLoader(_PRODUCT_NOTIFICATIONS_TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
    )

    msg = await create_user_email(env)

    async with create_email_session(settings) as smtp:
        await smtp.send_message(msg)
