something = [
    {
        "companyName": "Blizkasse",
        "companyAdress": "Musterstrasse",
        "companyZip": "12345",
        "companyCity": "01234 Musterstadt",
        "companyPhone": "0123/4567890",
        "companyOwner": "Franz Mustermann",
        "companyEmail": "muster@muster.muster",
        "companyTurnTaxId": "wird Beantragt",
        "startDate": "10.07.2023 13:08:21",
        "endDate": "10.07.2023 13:08:36",
        "entries":[]
    }
]



dict = {
    "key": something[0]["companyName"]
}

print(dict["key"])