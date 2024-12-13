import requests
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Learn_Backend_Concepts.settings')

from django.conf import settings


"""
"""
def send_email():
    # Hardcoded email addresses for testing
    recipient_list = ['kabugi96@gmail.com', 'kabugigu@gmail.com']
    
    subject = 'Test Email from Django Application'
    email_body = """
    Hello,
    
    This is a test email sent from the Django application.
    
    Best regards,
    Your Django App
    """
    
    try:
        send_mail(
            subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,  # Sender email configured in settings.py
            recipient_list,
            fail_silently=False,  # Set to False to raise exceptions on failure
        )
        print("Emails sent successfully.")
    except Exception as e:
        # Log the error for debugging
        print(f"Failed to send email: {e}")
if __name__ == '__main__':
    send_email()