import numpy as np
from backend.color_analysis import shift_complementary, shift_soft_complementary, shift_analogous
import sqlite3
import json
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "color_artworks.db"



def get_database_histograms():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.execute(
        "SELECT harvard_id, histogram FROM color_artworks"
    )

    harvard_ids = []
    histograms = []

    for harvard_id, histogram_json in cursor:
        harvard_ids.append(harvard_id)
        histograms.append(json.loads(histogram_json))

    connection.close()

    return np.array(harvard_ids), np.array(histograms)





def find_best_matches(query, relationship):
    harvard_ids, database = get_database_histograms()
    if relationship == "complementary":
        shifted_query = shift_complementary(query)
    elif relationship == "soft_complementary":
        shifted_query = shift_soft_complementary(query)
    elif relationship == "analogous":
        shifted_query = shift_analogous(query)
    elif relationship == "similar":
        shifted_query = query
    else:
        raise ValueError(f"Unknown relationship: {relationship}")

    if relationship == "analogous":

        distances_left = np.linalg.norm(
            database - shifted_query[0],
            axis=1
        )

        distances_right = np.linalg.norm(
            database - shifted_query[1],
            axis=1
        )

        distances = np.minimum(distances_left, distances_right)

    else:
        
        # Calculate the Euclidean distance between the shifted query and each histogram in the database
        distances = np.linalg.norm(database - shifted_query, axis=1)
        
    # Find the index of the histogram with the smallest distance
    best_match_indices = np.argsort(distances)[:3]  # Get the indices of the three closest matches
    \

    return harvard_ids[best_match_indices]
