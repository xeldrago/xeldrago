from truecallerpy import send_otp, verify_otp, search_phonenumber
import json

def request_installation_id(user_phone: str, country_code: str):
    response = send_otp(user_phone, country_code)
    data = json.loads(response)

    if data["status"] != 1:
        raise Exception(f"OTP failed to send: {data.get('message', 'Unknown error')}")
    
    request_id = data["data"]["requestId"]
    print(f"OTP sent to {user_phone}.")
    return request_id

def get_installation_id(request_id: str, otp: str, user_phone: str, country_code: str):
    response = verify_otp(request_id, otp, user_phone, country_code)
    data = json.loads(response)

    if data["status"] != 1:
        raise Exception(f"OTP verification failed: {data.get('message', 'Unknown error')}")
    
    return data["data"]["installationId"]

def truecaller_lookup(target_number, country_code, installation_id):
    try:
        response = search_phonenumber(target_number, country_code, installation_id)
        data = json.loads(response)

        if "data" not in data:
            return {"Error": "No data found or authentication failed."}

        info = data["data"]
        
        name = info.get("name", "N/A")
        phone_type = info.get("phones", [{}])[0].get("type", "N/A")
        spam_score = info.get("spamInfo", {}).get("spamScore", "N/A")
        carrier = info.get("phones", [{}])[0].get("carrier", "N/A")
        country = info.get("phones", [{}])[0].get("countryCode", "N/A")

        emails = [
            email.get("id") for email in info.get("internetAddresses", [])
            if email.get("id")
        ]
        email_list = ', '.join(emails) if emails else "N/A"

        return {
            "Name": name,
            "Phone Type": phone_type,
            "Spam Score": spam_score,
            "Carrier": carrier,
            "Country Code": country,
            "Associated Emails": email_list
        }

    except Exception as e:
        return {"Error": str(e)}


if __name__ == "__main__":
    print("=== Authenticate Your Truecaller Account ===")
    user_phone = input("Enter YOUR phone number (no + or country code): ").strip()
    user_country = input("Enter your 2-letter country code (e.g., IN): ").strip().upper()

    try:
        req_id = request_installation_id(user_phone, user_country)
        otp_input = input("Enter the OTP you received: ").strip()
        installation_id = get_installation_id(req_id, otp_input, user_phone, user_country)
        print("✅ Authentication Successful!\n")

        print("=== Lookup a Number ===")
        target_number = input("Enter the phone number to lookup: ").strip()
        target_country = input("Enter the target number's country code: ").strip().upper()

        result = truecaller_lookup(target_number, target_country, installation_id)

        print("\n=== Lookup Result ===")
        for k, v in result.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"❌ Error: {e}")
