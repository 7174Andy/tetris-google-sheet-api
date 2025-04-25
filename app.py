from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_DB_URI"))
if client is None:
    raise ValueError("MongoDB URI is not set in the environment variables")

db = client["test"]
collection = db["players"]


@app.route("/insert", methods=["POST"])
def insert_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Find the player by name in database
        player_name = collection.find_one({"name": data["name"]})

        if player_name:
            # If player exists, do not insert again
            # pass without error
            return jsonify({"message": "Player already exists"}), 200

        result = collection.insert_one(data)
        return jsonify({"message": "Data inserted", "id": str(result.inserted_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
