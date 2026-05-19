# Deployment Checklist

Use this checklist to ensure a smooth deployment of LinkoraX.

## Pre-Deployment

- [ ] Update `SECRET_KEY` in production `.env`
- [ ] Set `DEBUG=False` in production settings
- [ ] Configure `ALLOWED_HOSTS` with production domain
- [ ] Set up PostgreSQL database in production
- [ ] Configure email settings (SMTP)
- [ ] Set up Redis server
- [ ] Configure reCAPTCHA keys
- [ ] Update payment account details (JazzCash, Easypaisa, PayFast)
- [ ] Set up SSL certificate
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Configure monitoring and logging

## Server Setup

- [ ] Install Python 3.10+
- [ ] Install PostgreSQL
- [ ] Install Redis
- [ ] Install Nginx
- [ ] Create system user for application
- [ ] Set up virtual environment
- [ ] Install Python dependencies
- [ ] Configure environment variables
- [ ] Run database migrations
- [ ] Collect static files
- [ ] Initialize levels and achievements
- [ ] Create superuser account

## Application Configuration

- [ ] Configure Gunicorn systemd service
- [ ] Configure Celery systemd service
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL with Let's Encrypt
- [ ] Configure automatic SSL renewal
- [ ] Set up log rotation
- [ ] Configure error monitoring (Sentry, etc.)
- [ ] Set up uptime monitoring

## Security

- [ ] Enable HTTPS only
- [ ] Configure secure cookies
- [ ] Enable CSRF protection
- [ ] Configure rate limiting
- [ ] Set up fail2ban
- [ ] Configure firewall (ufw)
- [ ] Disable root SSH login
- [ ] Use SSH key authentication
- [ ] Regular security updates
- [ ] Monitor fraud detection logs

## Testing

- [ ] Test user registration
- [ ] Test email verification
- [ ] Test login/logout
- [ ] Test password reset
- [ ] Test payment submission
- [ ] Test referral system
- [ ] Test withdrawal request
- [ ] Test wallet transactions
- [ ] Test level progression
- [ ] Test support tickets
- [ ] Test admin panel
- [ ] Test mobile responsiveness

## Post-Deployment

- [ ] Monitor application logs
- [ ] Check database performance
- [ ] Monitor Redis connection
- [ ] Test email delivery
- [ ] Verify payment processing
- [ ] Check withdrawal processing
- [ ] Monitor fraud detection
- [ ] Set up alerts for errors
- [ ] Create backup schedule
- [ ] Document any issues

## Ongoing Maintenance

- [ ] Regular security updates
- [ ] Database backups (daily)
- [ ] Log rotation
- [ ] SSL certificate renewal
- [ ] Monitor disk space
- [ ] Monitor memory usage
- [ ] Review fraud logs weekly
- [ ] Update content regularly
- [ ] Respond to support tickets
- [ ] Monitor platform analytics

## Emergency Procedures

- [ ] Document rollback procedure
- [ ] Have backup restoration steps
- [ ] Emergency contact list
- [ ] Server access recovery
- [ ] Database recovery procedure
