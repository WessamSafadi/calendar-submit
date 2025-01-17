from flask import Flask, jsonify, request
import requests
import os
import urllib.parse

# Initialize Flask app
app = Flask(__name__)

# Function to fetch a new access token
def fetch_token():
    url = "https://apitest.leadperfection.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "password",
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "clientid": os.getenv("CLIENTID"),
        "appkey": os.getenv("APPKEY"),
    }

    try:
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"Failed to fetch token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None

# Book appointment endpoint
@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    access_token = fetch_token()  # Always fetch a new token
    if not access_token:
        return jsonify({"error": "Failed to fetch access token"}), 500

    request_data = request.json
    payload = {
        "firstname": request_data.get("firstname", ""),
        "lastname": request_data.get("lastname", ""),
        "phone": request_data.get("phone", ""),
        "zip": request_data.get("zip", ""),
        "apptdate": request_data.get("apptdate", ""),
        "appttime": request_data.get("appttime", ""),
        "recdDate": request_data.get("recdDate", ""),
        "recdTime": request_data.get("recdTime", ""),
        "notes": request_data.get("notes", ""),
        "crossStreet": request_data.get("crossStreet", ""),
        "waiver": request_data.get("waiver", "false"),
        "phone2": request_data.get("phone2", ""),
        "phone3": request_data.get("phone3", ""),
        "user1": request_data.get("user1", ""),
        "user2": request_data.get("user2", ""),
        "user3": request_data.get("user3", ""),
        "user4": request_data.get("user4", ""),
        "user5": request_data.get("user5", ""),
        "rnk_id": request_data.get("rnk_id", "0"),
        "datereceived": request_data.get("datereceived", ""),
        "state": request_data.get("state", ""),
    }

    # Encode payload for x-www-form-urlencoded
    encoded_payload = urllib.parse.urlencode(payload)

    url = "https://apitest.leadperfection.com/api/Leads/LeadAdd"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        response = requests.post(url, headers=headers, data=encoded_payload)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.text, "status": response.status_code}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
