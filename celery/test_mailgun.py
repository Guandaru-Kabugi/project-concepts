import requests
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


"""
def send_simple_message():
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox51922198327d4f83a64875a9e212637b.mailgun.org/messages",
        auth=("api", "6080df50948b0a8aa615077b4aff5293-da554c25-9e1ad0f8"),
        data={
            "from": "Excited User <mailgun@sandbox51922198327d4f83a64875a9e212637b.mailgun.org>",
            "to": ["guandarualex3@gmail.com", "sandbox51922198327d4f83a64875a9e212637b.mailgun.org"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!",
        },
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

send_simple_message()
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