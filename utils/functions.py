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

def create_email(subject, message, from_addr, to_addr, variables):
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
            La prédiction du modèle a été effectuée en utilisant des algorithmes de pointe et des pratiques standard de l'industrie. Nous vous assurons de la fiabilité de ces résultats, car ils ont subi des procédures de test et de validation rigoureuses.<br><br>
            Si vous avez des questions ou si vous avez besoin de plus d'informations, n'hésitez pas à nous contacter à tout moment.<br><br>
            Votre compréhension et votre coopération sont grandement appréciées.<br><br>
            Meilleures salutations,
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
        return message_body

def send_email(subject, message, from_addr, to_addr, password, variables):
    message_body = create_email(subject, message, from_addr, to_addr, variables)
    
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