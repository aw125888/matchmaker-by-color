from backend.harvard import get_harvard_paintings
from backend.database import create_database, save_artwork
from backend.color_analysis import get_pixels, build_histogram
import requests
from io import BytesIO
from PIL import Image
import time
from backend.harvard import api_key


def get_image_from_url(url, max_retries=3, sleep_seconds=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                headers={"AIC-User-Agent": "film-analysis"},
                timeout=30
            )
            response.raise_for_status()

            return Image.open(BytesIO(response.content))

        except requests.RequestException as error:
            print(
                f"Image download failed "
                f"(attempt {attempt + 1}/{max_retries}): {error}"
            )

            if attempt == max_retries - 1:
                return None

            time.sleep(sleep_seconds)


def populate_database():
    create_database()

    for page in get_harvard_paintings():
        for painting in page:
            print(f"Processing: {painting['name']}")

            image = get_image_from_url(painting["image_url"])

            if image is None:
                print("Skipping artwork.")
                continue

            pixels = get_pixels(image)
            histogram = build_histogram(pixels)
            image.close()

            save_artwork(painting, histogram)


populate_database()