from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import sys
import uuid
import shutil
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from background_removal import generate_mask, apply_mask, resize_and_format
from PIL import Image

app = FastAPI(title="Background Remover API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
MODELS_DIR = Path("models")

for directory in [UPLOAD_DIR, OUTPUT_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

@app.get("/")
@app.head("/")
async def root():
    return {"message": "Background Remover API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint - verifies API and model are ready"""
    model_path = MODELS_DIR / "u2net.pth"
    model_exists = model_path.exists()

    status = {
        "status": "healthy" if model_exists else "unhealthy",
        "api": "running",
        "model_loaded": model_exists,
    }

    if model_exists:
        file_size_mb = model_path.stat().st_size / (1024 * 1024)
        status["model_size_mb"] = round(file_size_mb, 1)
        status["model_path"] = str(model_path)

    return status

@app.post("/api/remove-background")
async def api_remove_background(
    file: UploadFile = File(...)
):
    """
    Step 1: Perform AI inference and create a high-res transparent "master" PNG
    """
    input_path = None
    master_path = None

    try:
        print(f"\n=== Background Removal (Inference Phase) ===")
        print(f"Filename: {file.filename}")

        # Validate file type
        allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file_ext}. Allowed: {', '.join(allowed_extensions)}"
            )

        unique_id = str(uuid.uuid4())
        input_filename = f"{unique_id}_input{file_ext}"
        master_filename = f"{unique_id}_master.png"

        input_path = UPLOAD_DIR / input_filename
        master_path = OUTPUT_DIR / master_filename

        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check if model exists
        model_path = MODELS_DIR / "u2net.pth"
        if not model_path.exists():
            raise HTTPException(status_code=500, detail="Model file not found.")

        # Process: Inference -> Apply Mask -> Save Master
        print("Starting AI inference...")
        mask = generate_mask(str(input_path), str(model_path))
        print("Applying mask...")
        master_image = apply_mask(str(input_path), mask)
        master_image.save(master_path, format="PNG")

        # Clean up input file
        input_path.unlink(missing_ok=True)

        return {
            "success": True,
            "master_file": master_filename,
            "message": "Background removed successfully"
        }

    except Exception as e:
        print(f"ERROR during inference: {str(e)}")
        if input_path and input_path.exists(): input_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prepare-download")
async def api_prepare_download(
    master_file: str = Form(...),
    resolution: str = Form("original"),
    format: str = Form("png")
):
    """
    Step 2: Resize and Format the master image for download
    """
    try:
        master_path = OUTPUT_DIR / master_file
        if not master_path.exists():
            raise HTTPException(status_code=404, detail="Master file not found")

        # Load master image — force RGBA to preserve transparency
        img = Image.open(master_path).convert('RGBA')
        
        # Post-process
        processed_img, save_format = resize_and_format(img, resolution, format)
        
        # Generate unique output filename
        unique_id = str(uuid.uuid4())
        out_ext = format.lower()
        if out_ext not in ["png", "webp"]: out_ext = "png"
        output_filename = f"{unique_id}_export.{out_ext}"
        output_path = OUTPUT_DIR / output_filename
        
        processed_img.save(output_path, format=save_format)
        
        return {
            "success": True,
            "output_file": output_filename,
            "message": "Image prepared for download"
        }
    except Exception as e:
        print(f"ERROR during export: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download processed image"""
    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Determine media type from extension
    ext = file_path.suffix.lower()
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }
    media_type = media_types.get(ext, "image/png")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )

@app.delete("/api/cleanup/{filename}")
async def cleanup_file(filename: str):
    """Delete processed file from server"""
    file_path = OUTPUT_DIR / filename

    if file_path.exists():
        file_path.unlink()
        return {"success": True, "message": "File deleted successfully"}

    return {"success": False, "message": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
