from fastapi import FastAPI, UploadFile, File, Form
from io import BytesIO
from PIL import Image 
import numpy as np
from pydantic import BaseModel

from backend.color_analysis import get_pixels, build_histogram, visualize_histogram
from backend.matching import find_best_matches
from backend.database import get_artworks_by_ids

from fastapi.middleware.cors import CORSMiddleware
 

class MatchRequest(BaseModel):
    histogram: list[float]
    relationship: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...), 

): 

    image_bytes = await image.read()
    pil_image = Image.open(BytesIO(image_bytes))

    pixels = get_pixels(pil_image)
    histogram = build_histogram(pixels)
    palette = visualize_histogram(histogram)

    return {
        "palette": palette,
        "histogram": histogram.tolist()
    }

@app.post("/match")
async def match(request: MatchRequest): 
    query = np.array(request.histogram)

    best_match_ids = find_best_matches(
        query, 
        request.relationship
    )

    artworks = get_artworks_by_ids(best_match_ids)
    print("BEST MATCH IDS:", best_match_ids)
    print("ARTWORKS RETURNED:", len(artworks))

    return {
        "matches": artworks
    }

