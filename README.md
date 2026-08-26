# Matchmaker by Hue 🎨

A full-stack visual artwork recommendation engine that matches your images with museum artworks through color.

Upload an image, choose a color relationship, and Matchmaker by Hue searches a preprocessed museum collection for three paintings whose color distributions best fit the relationship.

**Live Demo:** https://matchmaker-by-the-hue.vercel.app

---

## How It Works

Matchmaker represents both user-uploaded images and museum artworks as color distributions in HSV color space.

When an image is uploaded:

1. The image is converted into HSV color space.
2. Its pixels are summarized as a normalized **576-bin color histogram**.
3. The eight dominant histogram bins are converted back into RGB values to create a visual color palette.
4. The user chooses a color relationship.
5. The histogram is transformed according to that relationship.
6. The transformed histogram is compared against a preprocessed museum corpus using Euclidean distance.
7. The three closest artworks are returned as matches.

---

## Color Relationships

### Complementary
**Take a 180° dip.**

The query histogram is shifted approximately 180° around the hue wheel to search for artworks dominated by complementary colors.

### Analogous
**Play it safe with ±30°.**

Two target histograms are generated at +30° and -30°. Each artwork is compared against both targets, and its smaller distance is used for ranking.

### Similar
**It's good to be self-confident.**

No hue transformation is applied. The system searches directly for artworks with color distributions similar to the uploaded image.

### Soft-Complementary
**Tiny! Adventures!**

The histogram is shifted approximately 150°, producing a relationship that approaches complementary colors without going fully opposite on the hue wheel.

---

## Architecture

```text
                        USER IMAGE
                            │
                            ▼
                    React / TypeScript
                            │
                     POST /analyze
                            │
                            ▼
                         FastAPI
                            │
                  Pillow + NumPy
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        576-bin HSV histogram      8-color palette
                │
                ▼
         React ColorAnalysis
                │
        relationship selected
                │
                  POST /match
                │
                ▼
        histogram transformation
                │
                ▼
         Euclidean distance
                │
                ▼
       preprocessed SQLite corpus
                │
                ▼
          top three artworks
                │
                ▼
              React UI
```

---

## Museum Corpus

The recommendation corpus is built from artwork metadata and images provided by the **Harvard Art Museums**.

During preprocessing, each qualifying painting is:

- retrieved through the museum API,
- analyzed using the same HSV histogram representation as user uploads,
- assigned an eight-color dominant palette,
- and stored in SQLite with its metadata and image URL.

Because artwork histograms are calculated ahead of time, a user search does not need to reprocess the entire museum collection.

---

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- CSS
- Vercel

### Backend
- Python
- FastAPI
- NumPy
- Pillow
- SQLite
- Uvicorn
- Render

### Data
- Harvard Art Museums API

---

## API

### `POST /analyze`

Accepts an uploaded image.

Returns:

```json
{
  "palette": [
    [196, 224, 212],
    [120, 150, 180]
  ],
  "histogram": [
    0.0,
    0.012,
    0.031
  ]
}
```

The full histogram contains 576 normalized values.

---

### `POST /match`

Accepts a histogram and relationship:

```json
{
  "histogram": [0.0, 0.012, 0.031],
  "relationship": "complementary"
}
```

Supported relationships:

```text
complementary
analogous
similar
soft_complementary
```

Returns three ranked artwork matches with metadata, image URLs, and dominant color palettes.

## Deployment

The application is deployed as two services:

```text
Frontend
React + TypeScript + Vite
        │
        ▼
      Vercel


Backend
FastAPI + NumPy + SQLite
        │
        ▼
      Render
```

The production frontend communicates with the Render API for image analysis and artwork matching.

