# Exclusive Cars Automotive

Informatieve website voor autohandel - Een moderne Flask web applicatie voor een exclusieve autohandel.

## Beschrijving

Exclusive Cars Automotive is een professionele website voor een autohandel, gebouwd met Flask en Bootstrap 5. De website biedt een overzichtelijke presentatie van premium voertuigen met een moderne, donkere interface en rode accenten.

## Pagina's

- **Home**: Welkomstpagina met hero sectie en belangrijkste features
- **Aanbod**: Overzicht van alle beschikbare voertuigen
- **Auto Detail**: Gedetailleerde informatie per voertuig
- **FAQ**: Veelgestelde vragen met accordion functionaliteit
- **Contact**: Contactformulier met nieuwsbrief inschrijving voor 5% korting

## Features

✨ **Design**
- Donker grijze achtergrond met rode accenten
- Volledig responsive Bootstrap 5 design
- Simpele witte navigatiebalk
- Elegante footer met meerdere secties

🚗 **Functionaliteit**
- E-mail inschrijving voor 5% kortingscode
- 6 voorbeeld voertuigen (BMW, Mercedes, Audi, VW, Tesla, Porsche)
- Interactieve FAQ met Bootstrap accordion
- Flash messages voor gebruikersfeedback
- Jinja2 templating voor herbruikbare componenten

## Installatie

### Vereisten
- Python 3.7 of hoger
- pip (Python package manager)

### Stappen

1. Clone de repository:
```bash
git clone https://github.com/hamza-1034556/Exclusive-Cars-Automotive.git
cd Exclusive-Cars-Automotive
```

2. Installeer dependencies:
```bash
pip install -r requirements.txt
```

3. Start de applicatie:
```bash
# Development mode (met debug)
FLASK_DEBUG=true python app.py

# Production mode (zonder debug)
python app.py
```

4. Open je browser en ga naar:
```
http://localhost:5000
```

## Project Structuur

```
Exclusive-Cars-Automotive/
├── app.py                  # Flask applicatie
├── requirements.txt        # Python dependencies
├── static/
│   └── css/
│       └── style.css      # Custom CSS styling
├── templates/
│   ├── base.html          # Base template met navbar en footer
│   ├── home.html          # Homepage
│   ├── aanbod.html        # Aanbod overzicht
│   ├── car_detail.html    # Auto detail pagina
│   ├── faq.html           # FAQ pagina
│   └── contact.html       # Contact pagina
└── README.md
```

## Technologieën

- **Backend**: Flask 3.0.0
- **Frontend**: Bootstrap 5.3.0, Bootstrap Icons
- **Templating**: Jinja2
- **Styling**: Custom CSS met CSS variabelen

## Kleurenschema

- **Primary Red**: `#dc3545`
- **Dark Gray**: `#2a2a2a`
- **Medium Gray**: `#3a3a3a`
- **Light Gray**: `#4a4a4a`
- **Text Light**: `#e0e0e0`

## Toekomstige Uitbreidingen

- Database integratie voor auto's en klanten
- Daadwerkelijke e-mail verzending voor kortingscodes
- Admin panel voor het beheren van voertuigen
- Zoek- en filterfunctionaliteit
- Afbeeldingen uploaden voor voertuigen
- Contact formulier met e-mail notificaties

## Licentie

© 2024 Exclusive Cars Automotive. Alle rechten voorbehouden.

## Contact

Voor vragen of opmerkingen, neem contact op via:
- E-mail: info@exclusivecars.nl
- Telefoon: +31 20 123 4567
