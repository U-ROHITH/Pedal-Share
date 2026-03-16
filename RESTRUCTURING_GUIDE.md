# Pedal-Share Project Restructuring Documentation

## Overview
The Pedal Share project has been successfully restructured from a monolithic architecture to a modular, scalable Django application with proper separation of concerns and modern web development practices.

## Project Structure

### New Architecture

```
pedal_share/
├── apps/                          # Modular applications
│   ├── core/                      # Shared utilities & base models
│   ├── users/                     # User authentication & profiles
│   ├── cycles/                    # Cycle management & listings
│   ├── bookings/                  # Booking & reservation system
│   ├── payments/                  # Payment & wallet management
│   └── complaints/                # Support tickets system
├── static/                        # Static files (CSS, JS, images)
│   ├── css/                       # External stylesheets
│   │   ├── base.css              # Global styles
│   │   ├── navbar.css            # Navigation styling
│   │   ├── footer.css            # Footer styling
│   │   ├── cycles.css            # Cycle listing styles
│   │   ├── bookings.css          # Booking management styles
│   │   ├── payments.css          # Payment/wallet styles
│   │   ├── components.css        # Reusable components
│   │   └── profile.css           # Profile & personal pages
│   ├── js/                        # JavaScript files
│   │   └── main.js               # Main functionality
│   └── images/                    # Image assets
├── templates/                     # HTML templates
│   ├── base.html                 # Main template
│   ├── base/                      # Layout partials
│   │   ├── navbar.html           # Navigation include
│   │   └── footer.html           # Footer include
│   ├── auth/                      # Authentication templates
│   ├── cycles/                    # Cycle management templates
│   ├── bookings/                  # Booking templates
│   ├── payments/                  # Payment templates
│   ├── complaints/                # Complaint templates
│   ├── common/                    # Error pages (404, 500)
│   └── components/                # Reusable components
├── project1/                      # Django project config
│   ├── settings.py               # Updated with new apps
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
└── requirements.txt              # Python dependencies
```

## Key Changes

### 1. Modular Apps Structure

#### Core App
- **Purpose**: Shared utilities and base models
- **Key Models**: `BaseModel` (abstract base with timestamps)
- **Usage**: Inherited by all other models

#### Users App
- **Models**: 
  - `UserProfile` - Extended user info with wallet
- **Views**: 
  - `signin` - User login
  - `signup` - User registration
  - `signout` - User logout
  - `profile` - Profile management
- **Features**: User authentication, profile management, wallet balance

#### Cycles App
- **Models**:
  - `Cycle` - Bicycle property with pricing and availability
- **Views**:
  - `available_cycles` - List all available cycles with filtering
  - `cycle_detail` - View cycle details
  - `add_cycle` - Owner can add new cycle
  - `my_cycles` - Owner view their cycles
  - `edit_cycle`, `delete_cycle` - Cycle management
  - `toggle_cycle_availability` - Enable/disable cycle
- **Features**: Cycle listing, filtering, owner management

#### Bookings App
- **Models**:
  - `Booking` - Rental reservation with pricing
- **Views**:
  - `book_cycle` - Create booking
  - `my_bookings` - View user bookings
  - `booking_detail` - View booking details
  - `cancel_booking`, `complete_booking` - Booking management
- **Features**: Booking management, automatic price calculation

#### Payments App
- **Models**:
  - `Transaction` - Payment tracking
- **Views**:
  - `wallet` - View wallet & transaction history
  - `topup_wallet` - Add money to wallet
  - `payment_gateway` - Payment processing
  - `booking_checkout` - Booking payment
  - `pay_with_wallet` - Wallet payment
- **Features**: Wallet management, transaction tracking, payment processing

#### Complaints App
- **Models**:
  - `Complaint` - Support tickets
- **Views**:
  - `raise_complaint` - Create new complaint
  - `my_complaints` - View user complaints
  - `complaint_detail` - View complaint details
- **Features**: Support ticket system, issue tracking

### 2. External CSS Files

All CSS has been extracted from templates into organized, modular files:

- **base.css** - Global styles, variables, typography, buttons, forms
- **navbar.css** - Responsive navigation styling
- **footer.css** - Footer layout and styling
- **cycles.css** - Cycle card layouts, grid systems, filtering
- **bookings.css** - Booking cards, timeline, statistics
- **payments.css** - Wallet styling, transaction lists, payment forms
- **components.css** - Alerts, badges, modals, tabs, pagination
- **profile.css** - Profile pages, personal sections

### 3. Template Hierarchy

Organized into logical folders with proper Django template inheritance:

```
Templates Structure:
- base.html (main layout)
  └── Templates inherit from base.html
      - auth/ (signin, signup, profile)
      - cycles/ (list, add, edit, my_cycles)
      - bookings/ (list, confirm, detail)
      - payments/ (wallet, topup, checkout)
      - complaints/ (raise, list, detail)
      - common/ (404, 500 errors)
```

### 4. Django Features Implemented

- **Template Tags & Filters**: Proper Django template syntax
- **Static Files**: Using `{% load static %}` and `{% static '' %}`
- **Forms**: Django ModelForm and custom forms  
- **Authentication**: @login_required decorators
- **Views**: Function-based views with proper decorators
- **URL Routing**: Namespace-based URLs (e.g., `users:`, `cycles:`)
- **Admin Interface**: Customized admin classes for all models
- **Messages Framework**: User feedback notifications
- **Template Inheritance**: DRY principle with base templates

### 5. Bootstrap 5 & Font Awesome 6

- Upgraded from Bootstrap 4 to Bootstrap 5
- Using Font Awesome 6 icons
- Responsive design patterns
- Mobile-first approach

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Update Settings
Settings.py already updated with:
- New app registrations
- Template configurations
- Static/media file settings
- Message tags configuration

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Collect Static Files
```bash
python manage.py collectstatic
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## URL Routing

### Main Routes
- `/` - Home page
- `/auth/` - Authentication (signin, signup, profile)
- `/cycles/` - Cycle management
- `/bookings/` - Booking management
- `/payments/` - Wallet & payments
- `/complaints/` - Support tickets
- `/admin/` - Django admin

### Example URLs
- `/auth/signin/` - Sign in
- `/auth/profile/` - Profile page
- `/cycles/` - Available cycles
- `/cycles/add/` - Add new cycle
- `/cycles/my-cycles/` - My cycles
- `/bookings/my-bookings/` - My bookings
- `/payments/wallet/` - Wallet
- `/complaints/raise/` - Raise complaint

## Features Overview

### For Renters
- Browse and filter available cycles
- Book cycles for specific time periods
- Manage bookings (view, cancel, complete)
- Wallet management (add money, view history)
- Raise complaints/support tickets
- View profile and transaction history

### For Owners
- List their cycles
- Set pricing and availability
- View booking requests
- Earn from rentals
- Toggle cycle availability

### Admin Features
- Manage all users, cycles, bookings
- View and resolve complaints
- Track transactions
- Generate reports

## Best Practices Implemented

✓ **Separation of Concerns** - Each app handles specific functionality
✓ **DRY (Don't Repeat Yourself)** - Template inheritance, reusable components
✓ **Scalability** - Easy to add new features in new apps
✓ **Security** - CSRF protection, login required decorators
✓ **Performance** - Database indexes, query optimization
✓ **Maintainability** - Clear folder structure, proper naming
✓ **User Experience** - Responsive design, clear feedback
✓ **Code Organization** - Forms, models, views properly separated

## Future Enhancements

- API endpoints using Django REST Framework
- Real payment gateway integration
- Mobile app
- Advanced analytics dashboard
- Real-time notifications
- Email confirmations
- SMS updates
- Map integration for locations
- Rating & review system
- Rider history & statistics

## Migration Guide (From Old Structure)

1. Old `home` app still available at `/legacy/` for compatibility
2. New modular apps take precedence in URL routing
3. Database is shared - old and new data coexist
4. Gradual migration possible without losing data

## Support

For issues or questions, contact the development team or check documentation in individual app folders.

---

**Last Updated**: March 2024
**Version**: 2.0 (Restructured)
