from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def account_activation_email(email, email_token):
    subject = 'Welcome to Roomie Radar - Activate Your Account'
    from_email = 'Roomie Radar <noreply@roomieradar.com>'

    activation_link = f"{settings.SITE_URL}/accounts/activate/?token={email_token}"

    html_message = render_to_string(
        'email/activation_email.html',
        {'activation_link': activation_link}
    )

    plain_text = f"""
Welcome to Roomie Radar!

To activate your account, please click the link below:
{activation_link}

If you didn't create this account, please ignore this email.

Best regards,
The Roomie Radar Team
    """.strip()

    try:
        # Use a connection with timeout to prevent hanging
        connection = get_connection(timeout=10)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=from_email,
            to=[email],
            connection=connection,
            headers={
                'Reply-To': 'support@roomieradar.com',
            }
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        logger.info(f"Activation email sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send activation email to {email}: {str(e)}")
        return False


