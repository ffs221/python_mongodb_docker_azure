# from app import mail
from flask import render_template
import sendgrid
from app.config import config


def sent_activation_email(email, display_name, user_id, activation_code):
    from_email = config.FROM_EMAIL
    activation_email_template = config.ACTIVATE_EMAIL_TEMPLATE
    to_email = [(email, display_name)]
    message = sendgrid.Mail(from_email=from_email,  to_emails=to_email)
    
    
    message.dynamic_template_data = {
        "display_name": display_name,
        "user_id": user_id,
        "activation_code": activation_code
    }
    message.template_id = activation_email_template

    try:
        sg = sendgrid.SendGridAPIClient(config.SENT_GRID_API_KEY)
        response = sg.send(message)
        return str(response.status_code)

    except Exception as e:
        print("Error: {0}".format(e))

