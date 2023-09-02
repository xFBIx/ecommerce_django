from mailjet_rest import Client

MJ_APIKEY_PUBLIC = ""
MJ_APIKEY_PRIVATE = ""


def mail(vendor_email, vendor):
    API_KEY = MJ_APIKEY_PUBLIC
    API_SECRET = MJ_APIKEY_PRIVATE
    mailjet = Client(auth=(API_KEY, API_SECRET), version="v3.1")
    data = {
        "Messages": [
            {
                "From": {"Email": "bosm2023@outlook.com", "Name": "Sweet Pants"},
                "To": [{"Email": f"{vendor_email}", "Name": f"{vendor}"}],
                "Subject": "Subject",
                "TextPart": "Text",
            }
        ]
    }
    mailjet.send.create(data=data)
    print("Email sent")


mail("xxxfbixx@gmail.com", "hello")
