from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from io import BytesIO
from PIL import Image

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "Models/Ovarian/1/model.h5"
MODEL = None
CLASS_NAMES = [ "Ovarian_Cancer","Ovarian_Non_Cancer"]

@app.on_event("startup")
async def load_model():
    global MODEL
    try:
        # Print TensorFlow version
        print(f"TensorFlow version: {tf.__version__}")
        
        # Check if the model file exists
        if os.path.exists(model_path):
            print("Model file exists. Loading the model...")
            MODEL = tf.keras.models.load_model(model_path)
            print("Model loaded successfully.")
        else:
            print("Model file does not exist.")
    except Exception as e:
        print("Error loading model:", str(e))

@app.get("/", response_class=HTMLResponse)
async def get():
    content = """
    <html>
        <head>
            <title>Upload File</title>
            <script>
                async function uploadFile(event) {
                    event.preventDefault();
                    const fileInput = document.getElementById('file');
                    const formData = new FormData();
                    formData.append('file', fileInput.files[0]);

                    const response = await fetch('http://localhost:8000/uploadfile/', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    const resultDiv = document.getElementById('result');
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <p>Classification: ${result.classification}</p>
                            <p>Confidence: ${result.confidence}</p>
                        `;
                    } else {
                        resultDiv.innerHTML = `
                            <p>Error: ${result.error}</p>
                        `;
                    }
                }
            </script>
        </head>
        <body>
            <h1>Upload File for Classification</h1>
            <form onsubmit="uploadFile(event)">
                <input id="file" name="file" type="file" required>
                <input type="submit" value="Upload">
            </form>
            <div id="result"></div>
        </body>
    </html>
    """
    return HTMLResponse(content=content)

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        if MODEL is None:
            return {"error": "Model is not loaded"}
        
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        predictions = MODEL.predict(img_batch)
        print("Prediction: ",predictions)
        print("position 0: ",predictions[0])
        print("class name: ",np.argmax(predictions[0]))
        confidence = float(np.max(predictions))
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        
        print("confidence: ",confidence)
        print("predicted_class: ",predicted_class)

        return {"filename": file.filename, "classification": predicted_class, "confidence": confidence}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)