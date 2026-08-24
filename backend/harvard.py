import requests
import time
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("HARVARD_API_KEY")


def get_harvard_paintings(
    max_retries=3,
    sleep_seconds=1
):
    url = "https://api.harvardartmuseums.org/object"

    page = 1

    while True:
        params = {
            "apikey": api_key,
            "classification": "Paintings",
            "hasimage": 1,
            "size": 100,  # 100 per API request, NOT 100 total
            "page": page,
        }

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()
                break

            except requests.RequestException as error:
                print(
                    f"Page {page} failed "
                    f"(attempt {attempt + 1}/{max_retries}): {error}"
                )

                if attempt == max_retries - 1:
                    raise

                time.sleep(sleep_seconds)

        data = response.json()
        artworks = data["records"]

        if not artworks:
            break

        paintings = []

        for artwork in artworks:
            image_url = artwork.get("primaryimageurl")

            if not image_url:
                continue

            people = artwork.get("people") or []

            if people:
                artist = people[0].get("displayname") or "Unknown artist"
            else:
                artist = "Unknown artist"

            paintings.append({
                "harvard_id": artwork["id"],
                "name": artwork.get("title") or "Untitled",
                "artist": artist,
                "date": artwork.get("dated") or "",
                "image_url": image_url
            })

        print(f"Finished page {page}")

        yield paintings

        time.sleep(sleep_seconds)
        page += 1