# ImgPixel

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-19.2.0-blue)
![TypeScript](https://img.shields.io/badge/typescript-4.9.5-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)

A web application for AI-powered background removal using the U²-Net deep learning model. Built with React, TypeScript, and FastAPI.

## What It Does

ImgPixel processes images through a U²-Net neural network to segment foregrounds from backgrounds. The frontend handles drag-and-drop uploads and provides side-by-side comparison of results. The backend runs PyTorch inference and serves processed images through a REST API.

The application supports multiple export formats (PNG, JPG, WebP) and resolution scaling while maintaining aspect ratios. All processing happens server-side with optional GPU acceleration.

## Why It's Useful

- **Privacy-First**: All image processing happens on your own server - images never leave your infrastructure
- **Production-Ready**: FastAPI backend with proper error handling, file validation, and automatic cleanup
- **Flexible Export**: Choose from multiple formats and resolutions (Original, HD, Full HD, 4K)
- **GPU Accelerated**: Automatic CUDA detection for faster processing when available
- **Modern UI**: Interactive before/after slider and responsive design for all screen sizes
- **No API Keys Required**: Self-hosted solution with no external dependencies or rate limits

Perfect for e-commerce product photography, profile picture generation, design workflows, or learning about deep learning deployment.

## Getting Started

### Prerequisites

- **Node.js** 16+ and **npm**
- **Python** 3.8+
- **pip** package manager
- **Git**

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ObsCure9277/Background-Remover.git
cd Background-Remover
```

2. **Download the U²-Net model weights**

```bash
mkdir -p backend/models
curl -L -o backend/models/u2net.pth https://github.com/xuebinqin/U-2-Net/releases/download/1.0/u2net.pth
```

The model file is 176MB and contains the pre-trained weights.

3. **Set up the backend**

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

4. **Set up the frontend**

```bash
cd ../frontend
npm install
```

### Running the Application

Open two terminal windows:

**Terminal 1 - Backend:**

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
```

Backend runs at `http://localhost:5000`

**Terminal 2 - Frontend:**

```bash
cd frontend
npm start
```

Frontend runs at `http://localhost:3000`

### Basic Usage

1. Open `http://localhost:3000` in your browser
2. Drag and drop an image or click to upload (PNG, JPG, JPEG, GIF, BMP, WebP)
3. Select your preferred export format and resolution
4. Click "Remove Background"
5. Use the slider to compare original and processed images
6. Click "Download" to save the result

### API Usage

The backend exposes a REST API for programmatic access:

```bash
# Remove background from an image
curl -X POST "http://localhost:5000/api/remove-background" \
  -F "file=@image.jpg" \
  -F "resolution=original"

# Check API health
curl http://localhost:5000/health
```

**Response:**
```json
{
  "success": true,
  "output_file": "uuid_output.png",
  "message": "Background removed successfully"
}
```

View the full API documentation at `http://localhost:5000/docs` when the backend is running.

## Project Structure

```
1-ImgPixel/
├── backend/
│   ├── models/              # Pre-trained model weights
│   ├── outputs/             # Processed images
│   ├── uploads/             # Temporary uploaded images
│   ├── src/
│   │   ├── main.py                # FastAPI application
│   │   ├── background_removal.py  # Image processing logic
│   │   ├── u2net_model.py         # U²-Net architecture
│   │   ├── train.py               # Model training script
│   │   ├── setup_dataset.py       # Dataset preparation
│   │   └── data/                  # Training datasets
│   │       ├── images/
│   │       └── mask/
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.tsx       # Drag-and-drop upload
│   │   │   ├── ImageComparison.tsx   # Before/after slider
│   │   │   └── Export.tsx            # Export options
│   │   ├── App.tsx          # Main application
│   │   ├── App.css          # Styles
│   │   └── index.css        # Global styles
│   └── package.json         # Node dependencies
└── README.md
```

## Technical Details

### Frontend Architecture

The React application uses modern web APIs:

- [FormData API](https://developer.mozilla.org/en-US/docs/Web/API/FormData) for multipart file uploads
- [URL.createObjectURL()](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static) for client-side image previews
- [Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API) via [react-dropzone](https://react-dropzone.js.org/)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*) for theming
- [Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout) and [Media Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries) for responsive layout

**Key Dependencies:**
- [React 19.2.0](https://react.dev/) - UI framework
- [TypeScript 4.9.5](https://www.typescriptlang.org/) - Type safety
- [@img-comparison-slider/react](https://img-comparison-slider.sneas.io/) - Interactive comparison slider
- [lucide-react](https://lucide.dev/) - Icon library

### Backend Architecture

The Python backend implements:

- PyTorch model inference with automatic CUDA/CPU device detection
- Residual U-Net architecture with encoder-decoder structure and skip connections
- Bilinear upsampling for mask reconstruction
- Aspect ratio preservation during resolution scaling
- FastAPI async request handlers with proper error cleanup
- CORS middleware for cross-origin requests

**Key Dependencies:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern async web framework
- [PyTorch](https://pytorch.org/) - Deep learning inference
- [Pillow](https://python-pillow.org/) - Image manipulation
- [NumPy](https://numpy.org/) - Array operations
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

### Font Stack

System fonts: `-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif`

## Training Your Own Model

The repository includes a training script at [backend/src/train.py](backend/src/train.py). To train on custom data:

1. Prepare your dataset with images and corresponding masks
2. Place images in `backend/src/data/images/`
3. Place masks in `backend/src/data/mask/`
4. Run the training script:

```bash
cd backend
python src/train.py
```

Training logs are saved to `backend/runs/` for visualization with TensorBoard.

## Getting Help

- **Issues**: Open an issue on [GitHub Issues](https://github.com/ObsCure9277/Background-Remover/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/ObsCure9277/Background-Remover/discussions)
- **API Documentation**: Visit `http://localhost:5000/docs` when running the backend

## Maintainer

**ObsCure9277** - [GitHub Profile](https://github.com/ObsCure9277)

## Acknowledgments

- [U²-Net: Going Deeper with Nested U-Structure for Salient Object Detection](https://github.com/xuebinqin/U-2-Net) by Xuebin Qin et al.
- FastAPI and React communities


