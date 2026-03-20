# 🚲 Pedal Share

**Pedal Share** is a web app that lets students rent out their unused bicycles and earn money. It helps students share cycles on campus in a sustainable and cost-effective way.

## ✨ Features

- **User Authentication** — Sign up, log in, and manage accounts (email/password)
- **Google SSO** — One-click sign-in/sign-up with Google Identity Services
- **Cycle Listings** — Owners can list bicycles with price, description, and availability
- **Booking System** — Browse and book available cycles with flexible rental periods
- **Wallet System** — In-app wallet for payments, top-ups, and earnings tracking
- **Complaints** — Raise and track complaints for any booking issues
- **Responsive Design** — Works on desktop and mobile browsers

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2 (Python 3.13) |
| **Frontend** | Bootstrap 4, HTML, CSS, JavaScript |
| **Database** | SQLite (dev) |
| **Auth** | Django Auth + Google Identity Services (GIS) |
| **Static Files** | WhiteNoise |

## 📁 Project Structure

```
Pedal-Share-upgraded-/
├── apps/               # Django applications
│   ├── core/           # Base models and shared utilities
│   ├── users/          # Auth, Profiles, and Google SSO logic
│   ├── cycles/         # Bicycle listings and management
│   ├── bookings/       # Rental and booking logic
│   ├── payments/       # Wallet system and transactions
│   └── complaints/     # Feedback and support system
├── project1/           # Django project configuration (settings, URLs)
├── templates/          # Global HTML templates
├── static/             # Static assets (CSS, JS, Images)
├── data/               # Database seeds and initial data
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── .env                # Configuration for environment variables
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/YVK49/Pedal-Share-upgraded-.git
   cd Pedal-Share-upgraded-
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the server:**
   ```bash
   python manage.py runserver 4000
   ```

6. **Visit:** [http://localhost:4000](http://localhost:4000)

### Google SSO Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create an OAuth 2.0 Client ID (Web application)
3. Add these **Authorized JavaScript origins:**
   - `http://localhost:4000`
   - `http://127.0.0.1:4000`
4. Add these **Authorized redirect URIs:**
   - `http://localhost:4000/auth/google-callback/`
   - `http://127.0.0.1:4000/auth/google-callback/`
5. Copy the Client ID into your `.env` file

## 📄 License

This project is for educational purposes.
