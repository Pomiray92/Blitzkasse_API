import requests
import argparse

def reprint_last_receipt(reprint_count):
    reprint_receipt_url = "http://localhost:8001/ReprintLastReceipt/"
    try:
        for i in range(1, reprint_count + 1):
            response = requests.get(reprint_receipt_url)
            if response.status_code == 200:
                print(f"Receipt {i}/{reprint_count} printed successfully!")
            else:
                print("Failed to print last receipt. Status Code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reprint Last Receipt")
    parser.add_argument("reprint_count", nargs="?", type=int, default=1, help="Number of times to reprint the receipt")
    args = parser.parse_args()

    reprint_count = args.reprint_count
    reprint_last_receipt(reprint_count)