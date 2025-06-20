from flask import Flask, render_template, request
from mistralai import Mistral
import os
import base64
import mimetypes

app = Flask(__name__)

# Setting the API Key of Mistral AI
os.environ["MISTRAL_API_KEY"] = "iIigytIhF49wWjtwUlOJwhiNbpnnxHXh"
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

def load_image(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    base64_url = f"data:{mime_type};base64,{base64_encoded}"
    return base64_url

@app.route("/", methods=["GET", "POST"])
def I2T():
    text = None
    image_path = None

    if request.method == "POST":
        file = request.files.get("U_file")
        if file:
            filepath = "static/uploaded.jpg"
            file.save(filepath)

            # Convert image to base64 for Mistral
            image_url = load_image(filepath)

            # Mistral OCR
            ocr_response = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "image_url",
                    "image_url": image_url,
                },
            )
            text = ocr_response.pages[0].markdown
            image_path = filepath  

    return render_template("index.html", text=text, image_path=image_path)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)