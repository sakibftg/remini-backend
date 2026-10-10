from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/enhance")
async def enhance_image(
    mode: str = Form(...),
    scale: int = Form(...),
    image: UploadFile = File(...)
):
    input_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    output_filename = f"enhanced_{image.filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    shutil.copy(input_path, output_path) 

    return FileResponse(output_path, media_type="image/jpeg", filename=output_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)