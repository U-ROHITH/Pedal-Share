# Pedal Share - Project Overview

## 🚲 Project Introduction
**Pedal Share** is a web application designed to let students rent out their unused bicycles and earn money, while helping others easily find and rent cost-effective and sustainable transportation on campus. 

## 🛠 Tech Stack
- **Backend:** Python with the Django Framework (`v4.2.11`)
- **Frontend:** HTML, CSS, JavaScript (utilizing Bootstrap for styling)
- **Database:** SQLite3 (`db.sqlite3`)
- **Server Application / Middleware:** Gunicorn, Whitenoise (for serving static files), ASGI/WSGI configs. 

## 📁 Project Structure
The repository is structured as a standard Django project:
- **`project1/`**: This is the top-level configuration directory containing `settings.py`, root `urls.py`, `asgi.py`, and `wsgi.py`.
- **`home/`**: This is the main functional app directory containing the logic. It includes:
  - `models.py`: Database schemas.
  - `views.py`: Request handlers containing the backend logic for rendering pages and processing data.
  - `urls.py`: App-level routing and paths.
- **`Template/`**: Contains the frontend HTML views (e.g., `frontend.html`, `availablecycles.html`, `Login.html`, `PaymentGateway.html`, `wallet.html`).
- **`static/`**: Holds CSS, JS, and image assets.
- **`manage.py`**: The standard Django command-line execution file.
- **`Procfile` & `runtime.txt`**: Used for project deployment configuration (e.g., to platforms like Heroku).

## 🗄️ Database Models
The database architecture defined in `home/models.py` has a solid foundation comprising 4 main models:
1. **`UserProfile`**: Extends Django's native `User` model via a one-to-one relationship to add fields such as `full_name`, `phone`, and a `wallet_balance` field that defaults to ₹500.00. 
2. **`Cycle`**: Stores all details about listed bicycles: 
   - Information about the owner.
   - Specs (`cycle_type` such as regular, electric, mountain, or hybrid, `color`, `rating`).
   - Availability and pricing (`available_from`, `available_until`, `is_available`, `price_per_hour`).
3. **`Booking`**: Links a user to a cycle when rented. It calculates the `total_amount` based on requested `hours` and manages the state (`active`, `completed`, `cancelled`).
4. **`Transaction`**: Tracks `credit` and `debit` movements to maintain an audit trail for user wallets.

## ✨ Key Features
- **User Authentication**: Students can sign up, log in, and manage their accounts. System includes standard login, sign-in, and sign-out pages (`signin.html`, `signup.html`).
- **General/Information Pages**: Handles typical platform pages (`aboutus.html`, `contactus.html`, `help`, `raiseacomplaint.html`).
- **Cycle Listings & Owner Dashboard ("My Cycles")**: Owners can add, delete, or toggle the availability of their own cycles, listing them on the platform.
- **Browser & Booking System**: Students can browse `availablecycles.html` and book available cycles. The system handles booking, cancellation, and completion for rides.
- **Integrated Wallet & Payments**: A simulated on-platform wallet (`wallet.html`) is updated after transactions via a simulated payment gateway (`PaymentGateway.html`). Secure payments via Stripe/PayPal can be integrated here.

## 🚀 Getting Started
1. Clone the repository.
2. Ensure you have Python installed.
3. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
