import sqlite3
import json
import numpy as np
from backend.color_analysis import visualize_histogram
from pathlib import Path
import time 

DATABASE_PATH = Path(__file__).resolve().parent / "color_artworks.db"
def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS color_artworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        harvard_id INTEGER NOT NULL UNIQUE,
        name TEXT,
        artist TEXT,
        date TEXT,
        image_url TEXT NOT NULL,
        histogram TEXT NOT NULL
    )
""")

    connection.commit()
    connection.close()


def save_artwork(artwork, histogram):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT OR IGNORE INTO color_artworks (
            harvard_id,
            name,
            artist,
            date,
            image_url,
            histogram
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        artwork["harvard_id"],
        artwork["name"],
        artwork["artist"],
        artwork["date"],
        artwork["image_url"],
        json.dumps(histogram.tolist())
    ))

    connection.commit()
    connection.close()


def get_artworks_by_ids(harvard_ids):
    connection = sqlite3.connect(DATABASE_PATH)
    harvard_ids = [int(harvard_id) for harvard_id in harvard_ids]


    placeholders = ",".join("?" for _ in harvard_ids)

    query = f"""
        SELECT harvard_id, name, artist, date, image_url, histogram
        FROM color_artworks
        WHERE harvard_id IN ({placeholders})
    """

    cursor = connection.execute(query, harvard_ids)

    artworks_by_id = {}

    print("LOOKING FOR:", harvard_ids)

    for harvard_id in harvard_ids:
        row = connection.execute(
            "SELECT harvard_id, name FROM color_artworks WHERE harvard_id = ?",
        (   int(harvard_id),)
        ).fetchone()

        print("LOOKUP", int(harvard_id), "=>", row)


    for harvard_id, name, artist, date, image_url, histogram_json in cursor:
        histogram = np.array(json.loads(histogram_json))

        palette = visualize_histogram(histogram)

        time.sleep(1)


        artworks_by_id[harvard_id] = {
            "name": name,
            "artist": artist,
            "date": date,
            "image_url": image_url,
            "palette": palette
        }

        


    connection.close()

    artworks = []
    

    for harvard_id in harvard_ids:
        if harvard_id in artworks_by_id:
            artworks.append(artworks_by_id[harvard_id])

    return artworks


                       
                           
                           