from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'dev-secret-key-change-in-production'

# Sample car data
CARS = [
    {
        'id': 1,
        'name': 'BMW 3 Series',
        'year': 2022,
        'price': '€ 45.000',
        'image': 'bmw-3-series.jpg',
        'description': 'Luxe sedan met moderne technologie en uitstekende prestaties.',
        'mileage': '25.000 km',
        'fuel': 'Benzine',
        'transmission': 'Automaat'
    },
    {
        'id': 2,
        'name': 'Mercedes-Benz E-Class',
        'year': 2021,
        'price': '€ 52.000',
        'image': 'mercedes-e-class.jpg',
        'description': 'Elegante en comfortabele executive sedan met topklasse uitrusting.',
        'mileage': '35.000 km',
        'fuel': 'Diesel',
        'transmission': 'Automaat'
    },
    {
        'id': 3,
        'name': 'Audi A4',
        'year': 2023,
        'price': '€ 48.000',
        'image': 'audi-a4.jpg',
        'description': 'Sportieve sedan met verfijnde afwerking en geavanceerde technologie.',
        'mileage': '15.000 km',
        'fuel': 'Benzine',
        'transmission': 'Automaat'
    },
    {
        'id': 4,
        'name': 'Volkswagen Golf GTI',
        'year': 2022,
        'price': '€ 38.000',
        'image': 'vw-golf-gti.jpg',
        'description': 'Iconische hot hatch met sportieve prestaties en praktische ruimte.',
        'mileage': '20.000 km',
        'fuel': 'Benzine',
        'transmission': 'Handgeschakeld'
    },
    {
        'id': 5,
        'name': 'Tesla Model 3',
        'year': 2023,
        'price': '€ 55.000',
        'image': 'tesla-model-3.jpg',
        'description': 'Elektrische sedan met indrukwekkende range en cutting-edge technologie.',
        'mileage': '10.000 km',
        'fuel': 'Elektrisch',
        'transmission': 'Automaat'
    },
    {
        'id': 6,
        'name': 'Porsche Cayenne',
        'year': 2022,
        'price': '€ 85.000',
        'image': 'porsche-cayenne.jpg',
        'description': 'Luxe SUV met sportieve prestaties en premium afwerking.',
        'mileage': '18.000 km',
        'fuel': 'Benzine',
        'transmission': 'Automaat'
    }
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aanbod')
def aanbod():
    return render_template('aanbod.html', cars=CARS)

@app.route('/auto/<int:car_id>')
def car_detail(car_id):
    car = next((car for car in CARS if car['id'] == car_id), None)
    if car is None:
        flash('Auto niet gevonden.', 'danger')
        return redirect(url_for('aanbod'))
    return render_template('car_detail.html', car=car)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # In a real application, you would save this to a database
            flash('Bedankt! We hebben uw e-mailadres ontvangen. U ontvangt binnenkort uw kortingscode.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Vul alstublieft een geldig e-mailadres in.', 'danger')
    return render_template('contact.html')

if __name__ == '__main__':
    # Debug mode should be disabled in production
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
