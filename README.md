# LinkoraX - Community Membership Platform

A production-ready Django-based community membership platform with referral rewards, digital resources, and comprehensive member management features.

## Features

- **User Authentication**: Email verification, secure password management, optional phone verification
- **Referral System**: Two-level referral tracking with automatic commission calculations
- **Wallet System**: Internal wallet with transaction history and withdrawal management
- **Payment Processing**: Support for JazzCash, Easypaisa, and PayFast
- **Level System**: Gamified member levels with progressive commission rates
- **Member Resources**: Premium digital content including PDFs, videos, and guides
- **Blog System**: SEO-optimized blog with categories and comments
- **Support System**: Ticket-based support with admin management
- **Anti-Fraud**: Advanced fraud detection with IP tracking and suspicious activity monitoring
- **Admin Dashboard**: Comprehensive admin panel with analytics and management tools

## Tech Stack

- **Backend**: Python 3.10+, Django 5.0, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: HTML5, Tailwind CSS, Alpine.js
- **Task Queue**: Celery with Redis
- **Web Server**: Gunicorn + Nginx
- **Email**: SMTP with Django email backend

## Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Redis server
- pip and virtualenv

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd LinkoraX
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up PostgreSQL database**
```bash
createdb linkorax
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Initialize levels and achievements**
```bash
python manage.py shell
# Run the initialization script from docs/initial_data.py
```

9. **Start development server**
```bash
python manage.py runserver
```

10. **Start Celery worker (for background tasks)**
```bash
celery -A linkorax worker -l info
```

## Environment Variables

Key environment variables in `.env`:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: PostgreSQL configuration
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Email settings
- `REDIS_URL`: Redis connection string
- `RECAPTCHA_PUBLIC_KEY`, `RECAPTCHA_PRIVATE_KEY`: Google reCAPTCHA keys

## Project Structure

```
LinkoraX/
├── linkorax/           # Main Django project
│   ├── settings.py     # Project settings
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── celery.py       # Celery configuration
├── users/              # User authentication and profiles
├── referrals/          # Referral system
├── wallet/             # Wallet and transactions
├── payments/           # Membership payments
├── withdrawals/        # Withdrawal requests
├── levels/             # Level and achievement system
├── resources/          # Member resources
├── blog/               # Blog system
├── support/            # Support tickets
├── notifications/      # Notification system
├── fraud/              # Fraud detection
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard/      # Dashboard templates
│   ├── emails/         # Email templates
│   └── admin/          # Admin templates
├── static/             # Static files
├── media/              # User uploaded files
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── .env.example        # Environment variables template
```

## Deployment

### Ubuntu VPS Deployment

1. **Update system**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install dependencies**
```bash
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx redis-server -y
```

3. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE linkorax;
CREATE USER linkorax_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE linkorax TO linkorax_user;
\q
```

4. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/linkorax
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/LinkoraX/staticfiles/;
    }

    location /media/ {
        alias /path/to/LinkoraX/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/linkorax /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **Configure Gunicorn systemd service**
```bash
sudo nano /etc/systemd/system/linkorax.service
```

Add:
```ini
[Unit]
Description=LinkoraX Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/LinkoraX
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:linkorax.sock linkorax.wsgi:application

[Install]
WantedBy=multi-user.target
```

7. **Start services**
```bash
sudo systemctl start linkorax
sudo systemctl enable linkorax
sudo systemctl start redis
sudo systemctl enable redis
```

8. **Configure SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Security Considerations

- Always use `DEBUG=False` in production
- Set strong `SECRET_KEY`
- Use environment variables for sensitive data
- Enable HTTPS with SSL certificate
- Configure firewall rules
- Regular security updates
- Implement rate limiting
- Use reCAPTCHA for forms
- Monitor fraud detection logs

## AdSense Compliance

The platform is designed with Google AdSense policy compliance in mind:

- Professional SaaS-style design
- No misleading financial promises
- Clear disclaimer about earnings
- Original content structure
- Mobile-responsive design
- Fast loading pages
- Proper footer with legal pages
- Contact information visible
- Privacy policy and terms pages
- No scam-like wording or guarantees

## Support

For support, contact: support@linkorax.com

## License

Copyright © 2024 LinkoraX. All rights reserved.
