from mailjet_rest import Client

MJ_APIKEY_PUBLIC = "b7f3524a9dbc88bbe6d4c684abd0fd60"
MJ_APIKEY_PRIVATE = "7db34a3b4b68c6011b4aebbd4b684b25"

# MJ_APIKEY_PUBLIC = "53e52492564bd7b965a53e9ac345611a"
# MJ_APIKEY_PRIVATE = "3253cf095d0994000379a401297fecf6"

# MJ_APIKEY_PUBLIC = "f97f3e5ff37d27e280edfe7fa38e7b6f"
# MJ_APIKEY_PRIVATE = "5fd04d48834b2eba56edeab281462b6a"


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
