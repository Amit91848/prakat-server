import boto3
from botocore.exceptions import ClientError

from_address = 'phoenixalphainfo@gmail.com'


# def mail_report(to_address, report):
#     return {
#         'Source': from_address,
#         'Destination': {
#             'ToAddresses': [to_address],
#         },
#         'Message': {
#             'Subject': {
#                 'Data': 'AI Generated Report',
#                 'Charset': 'UTF-8',
#             },
#             'Body': {
#                 'Html': {
#                     'Data': f'''<!DOCTYPE html>
#                         <html>
#                         <head>
#                         <!-- Your HTML content here -->
#                         </head>
#                         <body>
#                         <!-- Your HTML content here -->
#                         { report }
#                         </body>
#                         </html>''',
#                 },
#             },
#         },
#     }


# def send_ses_email(email, email_token):
#     message = mail_report(email, email_token)
#     try:
#         response = ses.send_email(**message)
#         print(response)
#         return response
#     except Exception as e:
#         print(e)
#         return str(e)

class SesMailSender:
    """Encapsulates functions to send emails with Amazon SES."""

    def __init__(self, ses_client):
        """
        :param ses_client: A Boto3 Amazon SES client.
        """
        self.ses_client = ses_client

    # def send_email(self, source, destination, subject, text, html):
    def send_email(self, source, destination, subject, text):
        """
        Sends an email.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.

        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param text: The plain text version of the body of the email.
        :param html: The HTML version of the body of the email.
        :param reply_tos: Email accounts that will receive a reply if the recipient
                          replies to the message.
        :return: The ID of the message, assigned by Amazon SES.
        """
        send_args = {
            'Source': source,
            'Destination': destination,
            'Message': {
                'Subject': {'Data': subject},
                # 'Body': {'Text': {'Data': text}, 'Html': {'Data': html}}}}
                'Body': {'Text': {'Data': text}}}}
        try:
            response = self.ses_client.send_email(**send_args)
            message_id = response['MessageId']
            print(
                "Sent mail %s from %s to %s.", message_id, source)
        except ClientError:
            print(
                "Couldn't send mail from %s to %s.", source)
            raise
        else:
            return message_id
