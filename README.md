# ImgPixel

A web application for AI-powered background removal using the U²-Net deep learning model. Built with React, TypeScript, and FastAPI.

## Description

ImgPixel processes images through a U²-Net neural network to segment foregrounds from backgrounds. The frontend handles drag-and-drop uploads and provides side-by-side comparison of results. The backend runs PyTorch inference and serves processed images through a REST API.

The application supports multiple export formats (PNG, JPG, WebP) and resolution scaling while maintaining aspect ratios. All processing happens server-side with optional GPU acceleration.

## Techniques

The codebase demonstrates several patterns for building image processing applications:

**Frontend**
- [FormData API](https://developer.mozilla.org/en-US/docs/Web/API/FormData) for multipart file uploads to REST endpoints
- [URL.createObjectURL()](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static) for client-side image previews without server round-trips
- [Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API) via react-dropzone for file selection
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*) for theme management and consistent styling
- [Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout) and [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout) for responsive layouts
- [Media Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries) for mobile-responsive breakpoints
- [CSS Transforms](https://developer.mozilla.org/en-US/docs/Web/CSS/transform) and [Transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions) for button hover effects

**Backend**
- PyTorch model inference with CUDA/CPU device detection
- Residual U-Net architecture with encoder-decoder structure
- Bilinear upsampling for mask reconstruction
- Aspect ratio preservation during resolution scaling
- FastAPI async request handlers with proper cleanup on errors
- CORS middleware configuration for cross-origin requests

## Technologies

**Frontend Libraries**
- [React 19.2.0](https://react.dev/) - Component framework
- [TypeScript 4.9.5](https://www.typescriptlang.org/) - Type safety
- [react-dropzone 14.3.8](https://react-dropzone.js.org/) - Drag-and-drop file uploads
- [@img-comparison-slider/react 8.0.2](https://img-comparison-slider.sneas.io/) - Interactive before/after slider
- [lucide-react 0.552.0](https://lucide.dev/) - Icon library

**Backend Libraries**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [PyTorch](https://pytorch.org/) - Deep learning inference
- [Pillow](https://python-pillow.org/) - Image processing
- [NumPy](https://numpy.org/) - Array operations
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

**Fonts**
The application uses the system font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif` as defined in [index.css](frontend/src/index.css).

## Project Structure

```
1-ImgPixel/
├── backend/
│   ├── models/
│   ├── outputs/
│   ├── src/
│   │   └── data/
│   │       ├── images/
│   │       └── mask/
│   ├── uploads/
│   └── runs/
├── frontend/
│   ├── public/
│   └── src/
│       └── components/
├── README.md
├── package.json
└── requirements.txt
```

**backend/models/** - Pre-trained U²-Net weights (u2net.pth, 176MB)  
**backend/outputs/** - Processed images with removed backgrounds  
**backend/uploads/** - Temporary storage for uploaded images  
**backend/src/data/** - Training dataset storage (images and masks)  
**backend/runs/** - TensorBoard training logs  
**frontend/src/components/** - React components ([ImageUpload.tsx](frontend/src/components/ImageUpload.tsx), [ImageComparison.tsx](frontend/src/components/ImageComparison.tsx), [Export.tsx](frontend/src/components/Export.tsx))

The main application logic lives in [App.tsx](frontend/src/App.tsx) for the frontend and [main.py](backend/src/main.py) for the FastAPI server. Background removal processing is handled by [background_removal.py](backend/src/background_removal.py) using the U²-Net architecture defined in [u2net_model.py](backend/src/u2net_model.py).


