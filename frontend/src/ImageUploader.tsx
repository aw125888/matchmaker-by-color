import image1 from './assets/image1.jpg'
import image2 from './assets/image2.jpg'
import image3 from './assets/image3.jpg'
import image4 from './assets/image4.jpg'
import image5 from './assets/image5.jpg'
import image6 from './assets/image6.jpg'
import image7 from './assets/image7.jpg'
import image8 from './assets/image8.jpeg'
import image9 from './assets/image9.jpg'
import image10 from './assets/image10.jpg'
import image11 from './assets/image11.jpg'
import image12 from './assets/image12.jpg'
import image13 from './assets/image13.jpg'
import image14 from './assets/image14.jpg'
import image15 from './assets/image15.jpg'
import image16 from './assets/image16.jpg'
import image17 from './assets/image17.jpg'
import image18 from './assets/image18.jpg'
import image19 from './assets/image19.jpg'
import image20 from './assets/image20.jpg'
import image21 from './assets/image21.jpg'
import image22 from './assets/image22.jpg'
import image23 from './assets/image23.jpg'
import image24 from './assets/image24.jpg'
import image25 from './assets/image25.jpg'
import image26 from './assets/image26.jpg'
import image27 from './assets/image27.jpg'
import image28 from './assets/image28.jpg'
import image29 from './assets/image29.jpg'
import image30 from './assets/image30.jpg'
import { useEffect, useState} from 'react'
import './ImageUploader.css'

const images = [
  image17,
  image3,
  image24,
  image11,
  image29,
  image6,
  image20,
  image1,
  image14,
  image27,
  image9,
  image22,
  image5,
  image30,
  image16,
  image8,
  image25,
  image12,
  image2,
  image19,
  image28,
  image7,
  image15,
  image23,
  image4,
  image18,
  image10,
  image26,
  image13,
  image21
]

type ImageUploaderProps = {
  onAnalysisStart: () => void
  onAnalysisComplete: (palette: number[][], histogram: number[]) => void
}

function ImageUploader({onAnalysisComplete, onAnalysisStart}: ImageUploaderProps) {

    const [currentIndex, setCurrentIndex] = useState(0)
    const [uploadedImage, setUploadedImage] = useState<string | null>(null)

    const handleImageUpload = async (
        event: React.ChangeEvent<HTMLInputElement>
        ) => {
        const file = event.target.files?.[0]

        if (!file) {
            return
        }

        const imageURL = URL.createObjectURL(file)
        setUploadedImage(imageURL)

        const formData = new FormData()
        formData.append("image", file)

        onAnalysisStart()

        const response = await fetch("https://matchmaker-by-color.onrender.com/analyze", {
            method: "POST",
            body: formData,
        })

        if (!response.ok) {
            throw new Error("Image analysis failed")
        }

        const data = await response.json()

        onAnalysisComplete(data.palette, data.histogram)
        }
    

    useEffect(() => {

        if (uploadedImage) {
            return
        }
        const interval = setInterval(() => {
            setCurrentIndex((currentIndex) => (currentIndex + 1) % images.length)
        }, 250)
        return () => clearInterval(interval)
        }, [uploadedImage])

   return (
  <div className={`image-stage ${uploadedImage ? 'has-upload' : ''}`}>

    <input
    id ="image-input"
    type = "file"
    accept ="image/*"
    hidden
    onChange={handleImageUpload}
    />

  <img
    className="slideshow-image"
    src={images[currentIndex]}
    alt=""
  />

  {uploadedImage && (
    <img
      className="uploaded-image"
      src={uploadedImage}
      alt="Uploaded artwork"
    />
  )}

  {uploadedImage && (
    <div className="thanks">
      Thanks!
    </div>
  )}

  {!uploadedImage && (
    <label htmlFor="image-input" className="upload-button">
      +
    </label>
  )}
</div>
)
}



export default ImageUploader

