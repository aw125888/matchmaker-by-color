import './App.css'
import ImageUploader from './ImageUploader'
import { useState } from 'react'
import ColorAnalysis from './ColorAnalysis'



function App() {
  const [hasUploaded, setHasUploaded] = useState(false)
  const [palette, setPalette] = useState<number[][] | null>(null)
  const [histogram, setHistogram] = useState<number[] | null>(null)
  const [hasMatches, setHasMatches] = useState(false)
  const [uploadKey, setUploadKey] = useState(0)

  const handleStartOver = () => {
    setHasUploaded(false)
    setPalette(null)
    setHistogram(null)
    setHasMatches(false)

    setUploadKey((key) => key + 1)
  }

return (
    <main>
        <h1>
      MATCHMAKER{' '}
      <span className="by-color">
        (<span className="white">b</span><span className="blue">y</span> <span className="blue">p</span><span className="white">a</span><span className="blue">l</span><span className="white">e</span><span className="blue">t</span><span className="white">t</span><span className="white">e</span><span className="blue">!</span>)
      </span>
    </h1>
    <ImageUploader
    key={uploadKey}
    onAnalysisComplete={(palette, histogram) => {
    setPalette(palette)
    setHistogram(histogram)
    setHasUploaded(true)
  }}
/>

    <h2 className="instruction">
  <span className={`instruction-old ${hasUploaded ? 'fade-out' : ''}`}>
    The Matchmaker needs a matchee from you. Click the + and let's start the introductions.
  </span>

  {hasUploaded && !hasMatches && (
  <span className={`instruction-new ${hasMatches ? 'fade-out' : ''}`}>
    Matchee located: Choose your slice.
  </span>
)}


  {hasMatches && (
    <span className="instruction-new-new">
      Your ladies are ready for you!
    </span>
  )}
</h2>

{hasUploaded && palette && histogram && (
  <ColorAnalysis
    palette={palette}
    histogram={histogram}
    onMatchesReady ={( ) => setHasMatches(true)}
    onAgain= {() => setHasMatches(false)}
    onStartOver={handleStartOver}
  />
)}
    </main>
  )
}

export default App
