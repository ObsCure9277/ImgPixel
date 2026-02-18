# ImgPixel - AI Background Remover

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-19.2.0-blue)

A powerful web application that automatically removes backgrounds from images using **U²-NET** deep learning. Built with **React**, **TypeScript**, and **Python** (FastAPI) for a seamless and efficient user experience.

<img width="1889" height="950" alt="imgPixel_1" src="https://github.com/user-attachments/assets/546fd32c-39e3-4566-b4a7-4e7148dabd87" />
<img width="1889" height="948" alt="imgPixel_2" src="https://github.com/user-attachments/assets/326ecc82-24de-4447-938a-c4c0ded98d46" />

---

## 📋 Table of Contents

- [Why ImgPixel?](#-why-imgpixel)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Support](#-support)
- [License](#-license)

---

## 🎯 Why ImgPixel?

ImgPixel provides a professional-grade background removal tool that runs entirely on your infrastructure, ensuring:

- **Privacy**: Your images never leave your server
- **Quality**: Powered by the state-of-the-art U²-NET model
- **Flexibility**: Multiple export formats and resolution options
- **Speed**: Optimized for fast processing with GPU support
- **Ease of Use**: Intuitive drag-and-drop interface

Perfect for e-commerce product photos, profile pictures, social media content, and design projects.

---

## 🔑 Key Features

### ✅ Modern UI/UX
- **Responsive Design**: Optimized for all screen sizes
- **Drag & Drop Interface**: Easily upload images with drag-and-drop functionality
- **Error Handling**: Clear error messages for invalid inputs or processing failures
- **Side-by-Side Comparison**: Compare the original and processed images in real-time

### ✅ AI-Powered Background Removal
- Uses the state-of-the-art [U²-NET](https://github.com/xuebinqin/U-2-Net) deep learning model for precise background removal
- Supports multiple image formats: PNG, JPG, JPEG, GIF, BMP, WebP
- GPU acceleration support for faster processing

### ✅ Advanced Export Options
- **Format Selection**: Export images in PNG, JPG, or WebP formats
- **Resolution Options**: Choose from Original, HD (1280×720), Full HD (1920×1080), or 4K (3840×2160)
- **Smart Filenames**: Automatically generates filenames based on export settings

---

## 💻 Tech Stack

<table>
  <tr>
    <td>
      <b>Frontend:</b>
    </td>
    <td>
      <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
      <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" />
      <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
    </td>
  </tr>
  <tr>
    <td>
      <b>Backend:</b>
    </td>
    <td>
      <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
      <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
      <img src="https://img.shields.io/badge/FastAPI-109989?style=for-the-badge&logo=FASTAPI&logoColor=white" />
      <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" />
    </td>
  </tr>
</table>

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) and **npm**
- **Python** (3.8 or higher)
- **pip** (Python package manager)
- **Git**

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ObsCure9277/Background-Remover.git
cd Background-Remover
```

2. **Download the U²-NET Model**

Download the pre-trained U²-NET model and place it in the `backend/models/` directory:

```bash
# Create models directory
mkdir -p backend/models

# Download the model (176 MB)
# Visit: https://github.com/xuebinqin/U-2-Net#usage-for-salient-object-detection
# Or use wget/curl:
curl -L -o backend/models/u2net.pth https://github.com/xuebinqin/U-2-Net/releases/download/1.0/u2net.pth
```

3. **Install Backend Dependencies**

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

4. **Install Frontend Dependencies**

```bash
cd ../frontend
npm install
```

### Running the Application

You'll need to run both the backend and frontend servers.

**Terminal 1 - Backend Server:**

```bash
cd backend
# Activate virtual environment if not already active
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
```

The backend API will be available at `http://localhost:5000`

**Terminal 2 - Frontend Development Server:**

```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

---

## 📖 Usage

1. **Open the Application**: Navigate to `http://localhost:3000` in your web browser

2. **Upload an Image**: 
   - Drag and drop an image onto the upload area, or
   - Click the upload area to select an image from your computer

3. **Select Export Options**:
   - Choose your preferred format (PNG, JPG, or WebP)
   - Select the desired resolution (Original, HD, Full HD, or 4K)

4. **Remove Background**: Click the "Remove Background" button

5. **Compare Results**: View the original and processed images side-by-side

6. **Download**: Click "Download" to save the processed image

### Example API Usage

You can also use the API directly:

```bash
curl -X POST "http://localhost:5000/api/remove-background" \
  -F "file=@path/to/your/image.jpg" \
  -F "resolution=original"
```

---

## 📁 Project Structure

```
1-ImgPixel/
├── frontend/               # React TypeScript frontend
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Export.tsx           # Export options component
│   │   │   ├── ImageComparison.tsx  # Side-by-side comparison
│   │   │   └── ImageUpload.tsx      # Drag & drop upload
│   │   ├── App.tsx        # Main application component
│   │   └── App.css        # Application styles
│   └── package.json
│
├── backend/               # Python FastAPI backend
│   ├── src/
│   │   ├── main.py               # FastAPI application & routes
│   │   ├── background_removal.py # Background removal logic
│   │   ├── u2net_model.py        # U²-NET model architecture
│   │   ├── train.py              # Model training script
│   │   └── setup_dataset.py      # Dataset preparation
│   ├── models/            # U²-NET model weights
│   │   └── u2net.pth      # Pre-trained model (download required)
│   ├── uploads/           # Temporary uploaded images
│   ├── outputs/           # Processed images
│   └── requirements.txt   # Python dependencies
│
└── README.md
```

---

## 📚 API Documentation

### Endpoints

#### `GET /health`
Health check endpoint to verify API and model status.

**Response:**
```json
{
  "status": "healthy",
  "api": "running",
  "model_loaded": true,
  "model_size_mb": 176.3,
  "model_path": "models/u2net.pth"
}
```

#### `POST /api/remove-background`
Remove background from an uploaded image.

**Parameters:**
- `file` (multipart/form-data): Image file
- `resolution` (form): Target resolution (`original`, `hd`, `fullhd`, `4k`)

**Response:**
```json
{
  "output_file": "abc123_output.png",
  "message": "Background removed successfully"
}
```

#### `GET /api/download/{filename}`
Download a processed image.

For complete API documentation, start the backend server and visit: `http://localhost:5000/docs`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 💬 Support

If you encounter any issues or have questions:

- **GitHub Issues**: [Open an issue](https://github.com/ObsCure9277/Background-Remover/issues)
- **Discussions**: [Join the discussion](https://github.com/ObsCure9277/Background-Remover/discussions)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [U²-NET Model](https://github.com/xuebinqin/U-2-Net) by Xuebin Qin et al.
- FastAPI framework
- React and TypeScript communities

---

## 👨‍💻 Maintainer

**ObsCure9277** - [GitHub Profile](https://github.com/ObsCure9277)

---

<p align="center">Made with ❤️ by ObsCure9277</p>


