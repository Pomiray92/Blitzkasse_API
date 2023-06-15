import requests
import pdb


def get_client_info():
    klient_info_url = "http://localhost:8001/ConfigComplete"

    try:
        response = requests.get(klient_info_url)
        if response.status_code == 200:
            receipt_data = response.json()
            
            #print(f"CLIENT INFO:  {receipt_data}")
            companyName = receipt_data['companyName']
            companyAddress = receipt_data['companyAdress']
            companyCity = receipt_data['companyCity']
            companyTaxId = receipt_data['companyTaxId']
            companyEmail = receipt_data['companyEmail']
            companyPhone = receipt_data['companyPhone']

            # print("-----------------------------\n")
            # print(f"COMPANY NAME:  {companyName}")
            # print(f"COMPANY ADDRESS:  {companyAddress}")
            # print(f"COMPANY CITY:  {companyCity}")
            # print(f"COMPANY PHONE:  {companyPhone}")
            # print(f"COMPANY TAX ID:  {companyTaxId}")
            # print(f"COMPANY EMAIL:  {companyEmail}")
            # print("-----------------------------\n")
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

get_client_info()



def get_last_receipt():
    last_receipt_url = "http://localhost:8001/getLastReceipt"
    

    try:
        response = requests.get(last_receipt_url)
        if response.status_code == 200:
            receipt_data = response.json()
            
            get_table = receipt_data["levelDetailText"]
            # print(get_table)

            category_names = []
            for item in receipt_data["receiptItems"]:
                item_name = f"{item['name']} {item['count']}x {item['price']:.2f}"
                if item_name not in category_names:
                    category_names.append(item_name)
                else:
                    # Update the cost and quantity for existing item
                    existing_item_index = category_names.index(item_name)
                    existing_item = category_names[existing_item_index]
                    quantity = int(existing_item.split(" ")[-2][:-1]) + item["count"]
                    cost = float(existing_item.split(" ")[-1].replace(",", ".")) + (item["count"] * item["price"])
                    category_names[existing_item_index] = f"{item['name']} {quantity}x {cost:.2f}"
            
            


            #print(category_names)
            # Store the receipt data as per your requirements
            # Example: save it to a file, database, or variable
            # ...
            #print(receipt_data)
            receipt_number = receipt_data['receiptItems'][0]['receiptNumber']
            paymentOrderNumber = receipt_data['receiptItems'][0]['paymentOrderNumber']
            userName = receipt_data['receiptItems'][0]['userName']

            # print("User Name:", userName)
            # print("Payment Order Number:", paymentOrderNumber)
            # print("Receipt Number:", receipt_number)
            # print("-----------------------------\n")


            get_taxProducts = receipt_data["taxProducts"]

            tax_name_a = []
            tax_name_b = []
            tax_name_c = []

            for tax_product in get_taxProducts:
                if tax_product["totalBrutto"] != 0:
                    # Store the information in separate lists based on taxValue
                    tax_value = tax_product["taxValue"]
                    total_brutto = tax_product["totalBrutto"]
                    total_netto = tax_product["totalNetto"]
                    total_absolute_tax = tax_product["totalAbsoluteTax"]
                    name = tax_product["name"]
                    name_and_tax = f"{name} {tax_value}%"
                    if tax_value == 19:
                        tax_name_a.append({
                            " ": name_and_tax, 
                            "total_brutto": total_brutto,
                            "total_netto": total_netto,
                            "total_absolute_tax": total_absolute_tax
                        })
                    elif tax_value == 7:
                        tax_name_b.append({
                            " ": name_and_tax,
                            "total_brutto": total_brutto,
                            "total_netto": total_netto,
                            "total_absolute_tax": total_absolute_tax
                        })
                    elif tax_value == 0:
                        tax_name_c.append({
                            " ": name_and_tax,
                            "total_brutto": total_brutto,
                            "total_netto": total_netto,
                            "total_absolute_tax": total_absolute_tax
                        })

                    # Perform further processing or store the data as needed
                    print(f"Tax Value: {tax_value}")
                    print(f"Total Brutto: {total_brutto}")
                    print(f"Total Netto: {total_netto}")
                    print(f"Total Absolute Tax: {total_absolute_tax}")
                else:
                    # Skip to the next item
                    continue
            
            print(tax_name_a)
            print(tax_name_b)
            print(tax_name_c)

            #print("Last receipt data:", receipt_data)
            return receipt_data  # Return the receipt data
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

get_last_receipt()
