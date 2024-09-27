from django.core.mail import EmailMessage


class Util:
    def send_mail(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            to=[data["recipient"]]
        )
        email.send()

