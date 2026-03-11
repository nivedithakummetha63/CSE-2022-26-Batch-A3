from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def account_activation_email(email, email_token):
    subject = 'Welcome to Roomie Radar - Activate Your Account'
    from_email = 'Roomie Radar <noreply@roomieradar.com>'

    activation_link = f"{settings.SITE_URL}/accounts/activate/?token={email_token}"

    # Render HTML email template
    html_message = render_to_string(
        'email/activation_email.html',
        {'activation_link': activation_link}
    )

    # Plain text fallback
    plain_text = f"""
Welcome to Roomie Radar!

Thank you for joining our community of students finding their perfect roommates and ideal living spaces.

To activate your account, please click the link below:
{activation_link}

If you didn't create this account, please ignore this email.

Best regards,
The Roomie Radar Team
    """.strip()

    # Create email message
    msg = EmailMultiAlternatives(
        subject=subject,
        body=plain_text,
        from_email=from_email,
        to=[email],
        headers={
            'Reply-To': 'support@roomieradar.com',
            'X-Mailer': 'Roomie Radar System',
            'X-Priority': '1',
        }
    )
    
    # Attach HTML version
    msg.attach_alternative(html_message, "text/html")
    
    # Send email
    try:
        msg.send()
        logger.info(f"Activation email sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send activation email to {email}: {str(e)}")
        return False


