import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from .config import client


def validate_input(data):
    """
    Cette fonction valide les données entrées par l'utilisateur.
    Elle retourne True si toutes les données sont valides, sinon elle retourne False.
    """
    for value in data:
        # Vérifier si la valeur est numérique
        if not np.issubdtype(type(value), np.number):
            return False
        # Vérifier si la valeur est non négative
        if value < 0:
            return False
        
    return True


def convert_numpy_int64(document):
        for key, value in document.items():
            if isinstance(value, np.int64):
                document[key] = value.item()
        return document


def generate_html_table(variables):
        # Start of the table
        table = "<table>"

        # Column headers
        table += "<tr><th>Variable</th><th>Value</th><th>Description</th></tr>"

        # Add a row for each variable
        for var in variables:
            table += f"<tr><td>{var['name']}</td><td>{var['value']}</td><td>{var['description']}</td></tr>"

        # End of the table
        table += "</table>"

        return table


def send_email(subject, message, from_addr, to_addr, password, variables):
        # Create a multipart message
        message_body = MIMEMultipart("alternative")
        message_body["Subject"] = subject
        message_body["From"] = from_addr
        message_body["To"] = to_addr

        # Convert the message to HTML
        html_message = f"""
        <html>
        <body>
            <p>{message}</p>
            {generate_html_table(variables)}
            <p>
            The model prediction was carried out using top-notch algorithms and industry-standard practices. We assure you of the reliability of these results, as they have undergone rigorous testing and validation procedures.<br><br>
            Should you have any queries or require further information, please feel free to contact us at any time.<br><br>
            Your understanding and cooperation is greatly appreciated.<br><br>
            Best regards,
            </p>
        </body>
        </html>
        """

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        part1 = MIMEText(message, "plain")
        part2 = MIMEText(html_message, "html")
        message_body.attach(part1)
        message_body.attach(part2)

        # Sending the mail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, password)
        text = message_body.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()


def is_db_up():
    try:
        client.server_info() 
        return True
    except Exception as e:
        print(e)
        return False