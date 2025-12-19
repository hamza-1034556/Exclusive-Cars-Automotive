from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
import sqlite3
import secrets
import string
from datetime import datetime
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
            "img/cars/golf-85-r-carbon/01.png",
            "img/cars/golf-85-r-carbon/02.png",
            "img/cars/golf-85-r-carbon/03.png",
            "img/cars/golf-85-r-carbon/04.png",
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
        "images": ["img/cars/audi-rs3-2025/01.png"],
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


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


def generate_discount_code(prefix: str = "EC", length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}-{token}"


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Gmail SMTP.
    Vereist env vars:
      EMAIL_USER=exclusivecarsautoverhuur@gmail.com
      EMAIL_APP_PASSWORD=Google App Password (16 chars, zonder spaties)
    """
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_APP_PASSWORD")

    if not email_user or not email_pass or not to_email:
        return False

    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
        return True
    except Exception:
        return False


def send_admin_email(subject: str, body: str) -> bool:
    email_user = os.environ.get("EMAIL_USER")
    mail_to = os.environ.get("MAIL_TO") or email_user
    if not mail_to:
        return False
    return send_email(mail_to, subject, body)


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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        message = (request.form.get("message") or "").strip()
        wants_newsletter = 1 if request.form.get("newsletter") else 0

        if not is_valid_email(email):
            flash("Vul alstublieft een geldig e-mailadres in.", "danger")
            return redirect(url_for("contact"))

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Als checkbox uit staat, behandel dit als alleen een bericht (geen korting, geen DB insert)
        if wants_newsletter == 0:
            if message:
                send_admin_email(
                    subject=f"Nieuw bericht via contactformulier: {email}",
                    body=(
                        f"Naam: {name or '-'}\n"
                        f"E-mail: {email}\n"
                        f"Nieuwsbrief: nee\n\n"
                        f"Bericht:\n{message}\n\n"
                        f"Tijd: {now_str}\n"
                    ),
                )
                flash("Bedankt. Je bericht is verzonden.", "success")
            else:
                flash("Vink de nieuwsbrief aan voor welkomskorting, of vul een bericht in.", "danger")
            return redirect(url_for("contact"))

        # Nieuwsbrief staat aan, dan is het welkomskorting eenmalig
        with get_db() as conn:
            existing = conn.execute(
                "SELECT id, discount_code FROM newsletter_subscribers WHERE email = ?",
                (email,),
            ).fetchone()

            if existing:
                # Bestaand: geen nieuwe korting, geen code opnieuw tonen
                if message:
                    send_admin_email(
                        subject=f"Nieuw bericht via contactformulier (bestaand): {email}",
                        body=(
                            f"Naam: {name or '-'}\n"
                            f"E-mail: {email}\n"
                            f"Nieuwsbrief: ja (al ingeschreven)\n\n"
                            f"Bericht:\n{message}\n\n"
                            f"Tijd: {now_str}\n"
                        ),
                    )

                flash("Dit e-mailadres is al ingeschreven. Welkomskorting is eenmalig.", "danger")
                return redirect(url_for("contact"))

            # Nieuwe inschrijving
            discount_code = generate_discount_code()
            created_at = datetime.now().isoformat(timespec="seconds")

            conn.execute(
                """
                INSERT INTO newsletter_subscribers (email, name, message, wants_newsletter, discount_code, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (email, name or None, message or None, 1, discount_code, created_at),
            )
            conn.commit()

        # 1) Mail naar jou als er een bericht is ingevuld
        if message:
            send_admin_email(
                subject=f"Nieuw bericht via contactformulier: {email}",
                body=(
                    f"Naam: {name or '-'}\n"
                    f"E-mail: {email}\n"
                    f"Nieuwsbrief: ja\n"
                    f"Kortingscode: {discount_code}\n\n"
                    f"Bericht:\n{message}\n\n"
                    f"Tijd: {now_str}\n"
                ),
            )

        # 2) Mail naar klant met kortingscode
        mailed = send_email(
            to_email=email,
            subject="Exclusive Cars, jouw kortingscode (5%)",
            body=(
                f"Hi {name or 'daar'},\n\n"
                f"Bedankt voor je aanmelding bij Exclusive Cars.\n"
                f"Jouw kortingscode is: {discount_code}\n\n"
                f"Gebruik deze code bij je reservering.\n\n"
                f"Met vriendelijke groet,\n"
                f"Exclusive Cars\n"
                f"exclusivecarsautoverhuur@gmail.com\n"
            ),
        )

        if mailed:
            flash("Bedankt. Je aanmelding is ontvangen, je kortingscode is naar je e-mail gestuurd.", "success")
        else:
            flash(
                "Aanmelding opgeslagen. E-mail versturen is niet gelukt (controleer EMAIL_USER en EMAIL_APP_PASSWORD).",
                "danger",
            )

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
