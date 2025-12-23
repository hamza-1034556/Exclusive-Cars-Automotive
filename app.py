from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
import secrets
import string
from datetime import datetime, date
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

DB_PATH = os.path.join(os.path.dirname(__file__), "exclusivecars.db")


CARS = [
    {
        "id": 1,
        "name": "VW Golf 8.5R 2025 Special Black Edition Akrapovič",
        "year": 2025,
        "price_per_day": 350,
        "deposit": 1500,
        "min_age": 21,
        "km_included": "Km vrij",
        "location": "Rotterdam",
        "fuel": "Benzine",
        "transmission": "Automaat",
        "zero_to_hundred": 4.6,
        "top_speed": 270,
        "images": [
            "img/cars/golf-85-r-carbon/01.jpg",
            "img/cars/golf-85-r-carbon/02.jpg",
            "img/cars/golf-85-r-carbon/03.jpg",
            "img/cars/golf-85-r-carbon/04.jpg",
            "img/cars/golf-85-r-carbon/05.jpg",
            "img/cars/golf-85-r-carbon/06.jpg",
            "img/cars/golf-85-r-carbon/07.jpg",
        ],
        "description": (
            "Kracht, precisie en exclusiviteit komen samen in deze Black Edition.\n\n"
            "Met 333 pk accelereert de Golf 8.5R in slechts 4,6 seconden van 0 naar 100 km/u "
            "en bereikt hij met het R-Performance-pakket een topsnelheid tot 270 km/u.\n\n"
            "De Black Edition onderscheidt zich door zijn volledig donkere styling met zwarte 19 inch velgen, "
            "Akrapovič uitlaatsysteem en agressieve look aangevuld met carbon accenten.\n\n"
            "De Special modus, ontwikkeld voor de Nürburgring, optimaliseert het onderstel en aandrijving "
            "voor maximale prestaties op het circuit, terwijl het Harman Kardon premium audiosysteem zorgt "
            "voor een krachtige en zuivere geluidsbeleving.\n\n"
            "De perfecte performance hatch voor wie zich wil onderscheiden."
        ),
    },
    {
        "id": 2,
        "name": "Coming Soon...",
        "year": 2026,
        "price_per_day": 450,
        "deposit": 2500,
        "min_age": 23,
        "km_included": "Km vrij",
        "location": "Rotterdam",
        "fuel": "Benzine",
        "transmission": "Automaat",
        "zero_to_hundred": 3.2,
        "top_speed": 290,
        "images": [
            "img/cars/audi-rs3-2025/01.png",
        ],
        "description": "De koning van de hyper hatch, een legendarisch blok met het beste geluid van 2026.",
    },
]


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT,
                message TEXT,
                wants_newsletter INTEGER NOT NULL DEFAULT 0,
                discount_code TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def generate_discount_code(prefix: str = "EC", length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}-{token}"


def send_email(to_email: str, subject: str, body_text: str, body_html: str | None = None) -> bool:
    """
    Mailfunctie via Gmail SMTP.
    Vereist env vars:
      EMAIL_USER
      EMAIL_APP_PASSWORD (Gmail App Password)
    """
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_APP_PASSWORD")

    if not email_user or not email_pass or not to_email:
        return False

    msg = EmailMessage()
    msg["From"] = f"Exclusive Cars <{email_user}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.set_content(body_text)

    if body_html:
        msg.add_alternative(body_html, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
        return True
    except Exception:
        return False


def send_admin_email(subject: str, body_text: str, body_html: str | None = None) -> bool:
    email_user = os.environ.get("EMAIL_USER")
    mail_to = os.environ.get("MAIL_TO") or email_user
    if not mail_to:
        return False
    return send_email(mail_to, subject, body_text, body_html)


def looks_like_email(value: str) -> bool:
    v = (value or "").strip()
    return "@" in v and "." in v and " " not in v and len(v) <= 254


def build_external_url(endpoint: str, **values) -> str:
    """
    Biedt een stabiele base URL als je BASE_URL in .env zet (aanrader zodra je live staat).
    Anders valt terug op url_for(..., _external=True) op basis van de huidige request host.
    """
    base = (os.environ.get("BASE_URL") or "").strip().rstrip("/")
    if base:
        return base + url_for(endpoint, **values)
    return url_for(endpoint, _external=True, **values)


init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/aanbod")
def aanbod():
    return render_template("aanbod.html", cars=CARS)


@app.route("/auto/<int:car_id>")
def car_detail(car_id):
    car = next((c for c in CARS if c["id"] == car_id), None)
    if car is None:
        flash("Auto niet gevonden.", "danger")
        return redirect(url_for("aanbod"))
    return render_template("car_detail.html", car=car)


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/privacybeleid")
def privacybeleid():
    return render_template("privacybeleid.html", datum=date.today().strftime("%d-%m-%Y"))


@app.route("/algemene-voorwaarden")
def algemene_voorwaarden():
    return render_template("algemene_voorwaarden.html", datum=date.today().strftime("%d-%m-%Y"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        message = (request.form.get("message") or "").strip()
        wants_newsletter = 1 if request.form.get("newsletter") else 0

        if not looks_like_email(email):
            flash("Vul alstublieft een geldig e-mailadres in.", "danger")
            return redirect(url_for("contact"))

        with get_db() as conn:
            existing = conn.execute(
                "SELECT id, discount_code, created_at FROM newsletter_subscribers WHERE email = ?",
                (email,),
            ).fetchone()

            if existing:
                # Admin mail bij bericht, ook bij bestaande inschrijving
                if message:
                    admin_text = (
                        "Nieuw bericht via contactformulier (bestaande inschrijving)\n\n"
                        f"Naam: {name or '-'}\n"
                        f"E-mail: {email}\n"
                        f"Nieuwsbrief: {'ja' if wants_newsletter else 'nee'}\n"
                        f"Kortingscode (bestaand): {existing['discount_code']}\n"
                        f"Aangemeld op: {existing['created_at']}\n\n"
                        f"Bericht:\n{message}\n\n"
                        f"Tijd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    send_admin_email(
                        subject=f"Contactformulier (bestaand): {email}",
                        body_text=admin_text,
                    )

                flash(
                    f"Dit e-mailadres is al ingeschreven. Jouw kortingscode is: {existing['discount_code']}",
                    "success",
                )
                return redirect(url_for("contact"))

            # Nieuwe inschrijving
            discount_code = generate_discount_code()
            created_at = datetime.now().isoformat(timespec="seconds")

            conn.execute(
                """
                INSERT INTO newsletter_subscribers (email, name, message, wants_newsletter, discount_code, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    email,
                    name or None,
                    message or None,
                    wants_newsletter,
                    discount_code,
                    created_at,
                ),
            )
            conn.commit()

        # Admin mail als er een bericht is ingevuld
        if message:
            admin_text = (
                "Nieuw bericht via contactformulier\n\n"
                f"Naam: {name or '-'}\n"
                f"E-mail: {email}\n"
                f"Nieuwsbrief: {'ja' if wants_newsletter else 'nee'}\n"
                f"Kortingscode: {discount_code}\n\n"
                f"Bericht:\n{message}\n\n"
                f"Tijd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            send_admin_email(
                subject=f"Nieuw contactformulier: {email}",
                body_text=admin_text,
            )

        # Klant mail (HTML template als je die hebt)
        created_at_human = datetime.now().strftime("%d-%m-%Y %H:%M")

        # Let op: images via _external werken pas goed voor ontvangers als je site een publieke URL heeft.
        hero_image_url = build_external_url("static", filename="img/cars/golf-85-r-carbon/01.png")
        image_1_url = build_external_url("static", filename="img/cars/golf-85-r-carbon/02.png")
        image_2_url = build_external_url("static", filename="img/cars/golf-85-r-carbon/03.png")
        contact_url = build_external_url("contact")

        html_body = None
        try:
            html_body = render_template(
                "emails/discount_code.html",
                name=(name or "daar"),
                discount_code=discount_code,
                created_at=created_at_human,
                hero_image_url=hero_image_url,
                image_1_url=image_1_url,
                image_2_url=image_2_url,
                contact_url=contact_url,
            )
        except Exception:
            html_body = None

        text_body = (
            f"Hi {name or 'daar'},\n\n"
            "Bedankt voor je aanmelding bij Exclusive Cars.\n"
            f"Jouw kortingscode is: {discount_code}\n\n"
            "Gebruik deze code bij je reservering.\n\n"
            "Met vriendelijke groet,\n"
            "Exclusive Cars\n"
            "exclusivecarsautoverhuur@gmail.com\n"
        )

        send_email(
            to_email=email,
            subject="Exclusive Cars, jouw kortingscode (5%)",
            body_text=text_body,
            body_html=html_body,
        )

        flash(
            "Bedankt! We hebben je aanmelding ontvangen. Je kortingscode is naar je e-mail gestuurd.",
            "success",
        )
        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
