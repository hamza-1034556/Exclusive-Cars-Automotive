from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "dev-secret-key-change-in-production"

CARS = [
    {
        "id": 1,
        "name": "VW Golf 8.5R 2025 Special Black Edition Akrapovič",
        "year": 2025,

        # verhuur velden
        "price_per_day": 350,
        "deposit": 1500,
        "min_age": 21,
        "km_included": "Km vrij",
        "location": "Rotterdam",

        # auto info
        "fuel": "Benzine",
        "transmission": "Automaat",

        # performance
        "zero_to_hundred": 4.6,   # seconden
        "top_speed": 270,         # km/u

        # images
        "images": [
            "img/cars/golf-85-r-carbon/01.png",
            "img/cars/golf-85-r-carbon/02.png",
            "img/cars/golf-85-r-carbon/03.png",
            "img/cars/golf-85-r-carbon/04.png",
        ],

        "description": (
            "Kracht, precisie en exclusiviteit komen samen in deze Black Edition. "
            "Met 333 pk accelereert de Golf 8.5R in slechts 4,6 seconden van 0 naar 100 km/u "
            "en bereikt hij met het R-Performance-pakket een topsnelheid tot 270 km/u. "
            "De Black Edition onderscheidt zich door zijn volledig donkere styling met zwarte 19 inch velgen, "
            "Akrapovič uitlaatsysteem en agressieve look aangevuld met carbon accenten. "
            "De Special modus, ontwikkeld voor de Nürburgring, optimaliseert het onderstel en aandrijving "
            "voor maximale prestaties op het circuit, terwijl het Harman Kardon premium audiosysteem zorgt "
            "voor een krachtige en zuivere geluidsbeleving. De perfecte performance hatch voor wie zich wil onderscheiden."
        ),
    },
    {
        "id": 2,
        "name": "Coming Soon...",
        "year": 2026,

        # verhuur velden
        "price_per_day": 450,
        "deposit": 2500,
        "min_age": 23,
        "km_included": "Km vrij",
        "location": "Rotterdam",

        # auto info
        "fuel": "Benzine",
        "transmission": "Automaat",

        # performance (nog niet bekend, laat leeg of None)
        "zero_to_hundred": 3.2,
        "top_speed": 290,

        "images": [
            "img/cars/audi-rs3-2025/01.png",
        ],

        "description": "De koning van de hyper hatch, een legendarisch blok met het beste geluid van 2026.",
    },
]


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
        email = request.form.get("email")
        if email:
            flash(
                "Bedankt! We hebben uw e-mailadres ontvangen. U ontvangt binnenkort uw kortingscode.",
                "success",
            )
            return redirect(url_for("contact"))
        flash("Vul alstublieft een geldig e-mailadres in.", "danger")

    return render_template("contact.html")


if __name__ == "__main__":
    import os

    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
