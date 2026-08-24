import './ColorAnalysis.css'
import {useState} from 'react'


type ColorAnalysisProps = {
    palette: number[][]
    histogram: number[]
    onMatchesReady: () => void
    onAgain: () => void 
    onStartOver: () => void 
}

type Artwork = {
    name: string 
    artist: string
    date: string 
    image_url: string
    palette:number[][]
}

function ColorAnalysis({ palette, histogram, onMatchesReady , onAgain,onStartOver}: ColorAnalysisProps) {
    const [isSearching, setIsSearching] = useState(false)
    const [matches, setMatches] = useState<Artwork[]>([])
    

    const handleRelationship = async (relationship: string) => {
        setIsSearching(true)
        const response = await fetch ("https://matchmaker-by-color.onrender.com/match", {
            method: "POST", 
            headers: {
                "Content-Type": "application/json", 
            }, 
            body: JSON.stringify({
                histogram: histogram, 
                relationship: relationship, 
            })
        })

        if (!response.ok){
            throw new Error("Matching failed")
        }

        const data = await response.json()
        console.log("MATCH DATA:", data)
        console.log("IMAGES:", data.matches.map((artwork: Artwork) => artwork.image_url))
        onMatchesReady()

        setMatches(data.matches)
        setIsSearching(false)
    }

   
  return (
    <section className="color-analysis">

        {matches.length === 3 && (
            <div className="result-actions">
            <button
                className="again-button"
                onClick={() => {
                setMatches([])
                onAgain()
                }}
            >
                Again?
            </button>
                    <button
            className="start-over-button"
            onClick={onStartOver}
            >
            Or maybe start over?
            </button>
            </div>
            )}

      <div className="palette">
        {palette.map((color, index) => (
          <div
            key={index}
            className="palette-color"
            style={{
              backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})`,
            }}
          />
        ))}
      </div>

      {!isSearching && matches.length ===0 && (
         <div className="relationship-buttons">
        <div className="relationship-option">
          <button onClick={() => handleRelationship("complementary")}>
            Complementary

            </button>

            
          <p>take a 180° dip</p>
        </div>

        <div className="relationship-option">
          <button onClick={() => handleRelationship("analogous")}>Analogous</button>
          <p>play it safe with ±30°</p>
        </div>

        <div className="relationship-option">
          <button onClick={() => handleRelationship("similar")}>Similar</button>
          <p>it's good to be self-confident</p>
        </div>

        <div className="relationship-option">
          <button onClick={() => handleRelationship("soft_complementary")}>Soft-complementary</button>
          <p>tiny! adventures!</p>
        </div>
      </div>

      )}

      {isSearching && (
        <div className ="searching">
            Searching...
        </div>
      )}

      {!isSearching && matches.length > 0 && (
        <div className="match-results">
  {matches.map((artwork, index) => (
    <div
        key={index}
      className="match-card"
    >
      <img
  src={artwork.image_url}
  alt={artwork.name}
/>

      <div className = "match-info">
        <h3>{artwork.name} </h3>
        <p>{artwork.artist}</p>
        <p>{artwork.date}</p>

        <div className="match-palette">
          {artwork.palette.map((color, colorIndex) => (
            <div
              key={colorIndex}
              style={{
                backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})`,
              }}
            />
          ))}
        </div>
      </div>
    </div>
  ))}
</div>
      )}

     

    </section>
  )
}

export default ColorAnalysis