import pieces
from gvars import *
def send_email(EmailTo, Subject,Body,Co=None,output_path=None, nameFile=None):
    try:
        pieces.lib_logging.logger.info("[INICIO] send_email()")

        # Configurações do email
        receiver_email = EmailTo
        subject = Subject
        # Criar objeto MIMEMultipart
        msg = pieces.MIMEMultipart()
        # Dividir a string em uma lista de emails
        #receiver_email = EmailTo.split(';')
        # Adicionar as partes do email (texto e anexo)
        msg['From'] = EMAIL_USER
        #if len(receiver_email) > 1:
        msg['To'] = EmailTo  # Concatena os endereços separados por vírgula  
        msg['Co'] = Co
        #else:
        #msg['To'] = receiver_email[0]
        msg['Subject'] = subject
        # Corpo do email (texto)
        msg.attach(pieces.MIMEText(Body, 'plain'))
        if output_path:
            # Anexo
            with open(output_path, 'rb') as file:
                part = pieces.MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
            pieces.encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={nameFile}')
            msg.attach(part)

        # Enviar o email
        # Conectar ao servidor SMTP
        servidor = pieces.smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
        servidor.starttls()
        servidor.login(EMAIL_USER, EMAIL_PASS)

        # Enviar a mensagem
        servidor.send_message(msg)
        print('Email enviado com sucesso!')
    except Exception as error:
        pieces.lib_logging.logger.info(f"> send_email error message: {error}")
    finally:
        pieces.lib_logging.logger.info("[FIM] send_email()")