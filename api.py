from flask import Flask, jsonify
from flask_cors import CORS
import requests
import sqlite3
from dotenv import dotenv_values

app = Flask(__name__)
CORS(app)

config = dotenv_values(".env")

TOKEN = config["TOKEN"]

def incrementar_visitas():
    conn = sqlite3.connect("views.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            views INTEGER
        )
    """)

    cursor.execute("SELECT views FROM stats WHERE id = 1")
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO stats (id, views) VALUES (1, 0)")
        views = 0
    else:
        views = row[0]

    views += 1

    cursor.execute(
        "UPDATE stats SET views = ? WHERE id = 1",
        (views,)
    )

    conn.commit()
    conn.close()

    return views

@app.route("/")
def home():
    return "<h1>MOSCOUAPIS.COM</h1>"

@app.route("/profile/<userid>")
def perfil(userid):
    headers = {
        "Authorization": TOKEN
    }

    url = f"https://discord.com/api/v9/users/{userid}/profile"

    response = requests.get(url, headers=headers)

    data = response.json()

    data["views"] = incrementar_visitas()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)