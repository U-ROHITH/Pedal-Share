# PedalShare

**PedalShare** is an open-source campus bicycle sharing platform built with Django. Students can list their idle bicycles for rent and earn money, while others can book them for short rides — making campus commutes greener, cheaper, and more connected.

> Open source. Built by students, for students. Contributions welcome from anyone.

---

## Features

- **User Accounts** — Email/password signup and login, extended profile with wallet and ratings
- **Google SSO** — One-click sign-in via Google Identity Services (GIS)
- **Cycle Listings** — List bicycles with type, price per hour, availability schedule, and images
- **Booking System** — Browse, filter, and book cycles with automatic price calculation
- **Wallet & Payments** — In-app wallet with top-up, booking payments, earnings, and transaction history
- **Complaints & Support** — File support tickets linked to bookings or cycles, track resolution status
- **Responsive UI** — Bootstrap 4, mobile-friendly, custom CSS per module

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Python 3.12+ |
| Frontend | Bootstrap 4, HTML5, CSS3, Vanilla JS |
| Auth | Django Auth + Google Identity Services |
| Database | SQLite (dev) — PostgreSQL ready |
| Static Files | WhiteNoise (compressed + cached) |
| Deployment | Gunicorn, Heroku / Render / Railway |

---

## Project Structure

```
PedalShare/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── project1/               # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                   # All Django apps (modular)
│   ├── core/               # Base model, context processors, static pages
│   ├── users/              # Auth, profiles, Google SSO
│   ├── cycles/             # Bicycle listings and management
│   ├── bookings/           # Rental bookings
│   ├── payments/           # Wallet and transactions
│   └── complaints/         # Support and feedback
│
├── templates/              # HTML templates per app
├── static/                 # CSS, JS, images
└── data/                   # Seed data and historical DB
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip or a virtual environment tool

### Installation

```bash
git clone https://github.com/U-ROHITH/Pedal-Share.git
cd Pedal-Share

python -m venv env
source env/bin/activate        # Windows: env\Scripts\activate

pip install -r requirements.txt

cp .env.example .env           # then fill in your values
python manage.py migrate
python manage.py runserver 4000
```

Open [http://localhost:4000](http://localhost:4000)

### Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

### Google SSO Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create an **OAuth 2.0 Client ID** (Web application)
3. Add **Authorized JavaScript origins:** `http://localhost:4000`
4. Add **Authorized redirect URIs:** `http://localhost:4000/auth/google-callback/`
5. Paste the Client ID into your `.env`

### Seed Sample Data

```bash
python manage.py seed_data
```

---

## URL Reference

| Area | Endpoints |
|---|---|
| Auth | `/auth/signin/` `/auth/signup/` `/auth/profile/` `/auth/google-callback/` |
| Cycles | `/cycles/` `/cycles/add/` `/cycles/detail/<id>/` `/cycles/my-cycles/` |
| Bookings | `/bookings/book/<id>/` `/bookings/my-bookings/` `/bookings/detail/<id>/` |
| Payments | `/payments/wallet/` `/payments/topup/` `/payments/checkout/<id>/` |
| Complaints | `/complaints/raise/` `/complaints/my-complaints/` |
| Pages | `/about/` `/help/` `/contact/` |

---

## Contributing

PedalShare is fully open source. Anyone — students, developers, designers — is welcome to contribute.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push and open a Pull Request

Ideas for contribution: PostgreSQL integration, real payment gateway (Razorpay/Stripe), mobile app API, email notifications, map-based cycle search, admin dashboard improvements.

---

## License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

**Made with care for sustainable campus mobility. Come build with us.**
