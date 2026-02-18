# 🖼️ ImgPixel

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-19.2.0-blue)
![TypeScript](https://img.shields.io/badge/typescript-4.9.5-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)

**ImgPixel** is a powerful web application for AI-powered background removal using the U²-Net deep learning model. Built with React, TypeScript, and FastAPI, it offers a privacy-first solution where all image processing happens locally on your machine.


---

## 📋 Table of Contents

- [🔑 Key Features](#-key-features)
- [🚀 Getting Started](#-getting-started)
- [📂 Project Structure](#-project-structure)
- [💡 Usage Examples](#-usage-examples)
- [🛠️ Technical Details](#-technical-details)
- [🧠 Training Your Own Model](#-training-your-own-model)
- [📞 Support](#-support)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🔑 Key Features

### ✅ Privacy-First
- All image processing happens on your local server. Images never leave your infrastructure, ensuring complete data privacy and security.

### ✅ Production-Ready
- Powered by a robust FastAPI backend with proper error handling, file validation, and automatic temporary file cleanup to keep your storage managed.

### ✅ Flexible Export
- Choose from multiple export formats (PNG, JPG, WebP) and resolutions (Original, HD, Full HD, 4K) while maintaining aspect ratios.

### ✅ GPU Accelerated
- Automatically detects and utilizes NVIDIA GPUs (CUDA) for faster processing, seamlessly falling back to CPU when unavailable.

### ✅ Modern UI
- Features a clean, responsive interface with drag-and-drop uploads and an interactive before/after comparison slider to verify results instantly.

### ✅ No API Keys Required
- A completely self-hosted solution. No external API subscriptions, rate limits, or hidden costs.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- **Node.js**: v16 or higher
- **Python**: v3.8 or higher
- **Git**

### Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/ObsCure9277/ImgPixel.git
    cd ImgPixel
    ```

2.  **Download the U²-Net model weights**

    Download the pre-trained model (176MB) and place it in the `backend/models` directory:

    ```bash
    # Windows (PowerShell)
    mkdir -Force backend\models
    curl -L -o backend\models\u2net.pth https://github.com/xuebinqin/U-2-Net/releases/download/1.0/u2net.pth

    # macOS/Linux
    mkdir -p backend/models
    curl -L -o backend/models/u2net.pth https://github.com/xuebinqin/U-2-Net/releases/download/1.0/u2net.pth
    ```

3.  **Set up the backend**

    ```bash
    cd backend
    python -m venv venv

    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

    pip install -r requirements.txt
    ```

4.  **Set up the frontend**

    ```bash
    cd ../frontend
    npm install
    ```

### Running the Application

You'll need two terminal windows - one for the backend and one for the frontend.

**Terminal 1 - Backend Server:**

```bash
cd backend
# Activate virtual environment (if not already active)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
```
Backend runs at `http://localhost:5000`

**Terminal 2 - Frontend Dev Server:**

```bash
cd frontend
npm start
```
Frontend runs at `http://localhost:3000`

---

## 📂 Project Structure

```
ImgPixel/
├── backend/
│   ├── models/              # Pre-trained U²-Net model weights
│   ├── outputs/             # Processed images
│   ├── uploads/             # Temporary uploads
│   ├── src/
│   │   ├── main.py                # FastAPI application
│   │   ├── background_removal.py  # Inference logic
│   │   ├── u2net_model.py         # Neural network architecture
│   │   └── ...
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.tsx       # Drag-and-drop area
│   │   │   ├── ImageComparison.tsx   # Before/after slider
│   │   │   ├── Export.tsx            # Export options
│   │   └── App.tsx
│   └── package.json
└── README.md
```

---

## 💡 Usage Examples

### Basic Usage

1.  Open `http://localhost:3000` in your browser.
2.  **Upload**: Drag and drop an image or click to select.
3.  **Configure**: Select your desired format (PNG, JPG, WebP) and resolution.
4.  **Process**: Click "Remove Background".
5.  **Download**: Use the slider to compare, then click "Download" to save.

### API Usage

You can also use the backend purely as an API:

**Remove background from an image:**

```bash
curl -X POST "http://localhost:5000/api/remove-background" \
  -F "file=@image.jpg" \
  -F "resolution=original"
```

**Response:**
```json
{
  "success": true,
  "output_file": "uuid_output.png",
  "message": "Background removed successfully"
}
```

---

## 🛠️ Technical Details

### Architecture
- **Frontend**: React 19, TypeScript, Create React App
- **Backend**: Python 3.8+, FastAPI
- **AI Model**: U²-Net (PyTorch)
- **Image Processing**: Pillow (PIL), NumPy

### Model Information
- **Name**: U²-Net (Nested U-Structure)
- **Task**: Salient Object Detection
- **Input Size**: 320x320 (automatically resized)
- **Output**: Binary probability mask

---

## 🧠 Training Your Own Model

The repository includes scripts to train the model on your own dataset.

1.  **Prepare Data**: Place images in `backend/src/data/images/` and masks in `backend/src/data/mask/`.
2.  **Train**:
    ```bash
    cd backend
    python src/train.py
    ```
3.  **Visualize**:
    ```bash
    tensorboard --logdir=backend/runs
    ```

---

## 📞 Support

- **Issues**: Report bugs or suggest features on [GitHub Issues](https://github.com/ObsCure9277/ImgPixel/issues).
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/ObsCure9277/ImgPixel/discussions).
- **Docs**: Visit `http://localhost:5000/docs` for interactive API documentation when running the backend.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [U²-Net: Going Deeper with Nested U-Structure for Salient Object Detection](https://github.com/xuebinqin/U-2-Net) by Xuebin Qin et al.
- The open source communities behind FastAPI, React, and PyTorch.

---

**Made with ❤️ by [ObsCure9277](https://github.com/ObsCure9277)**

