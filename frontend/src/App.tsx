import "./App.css";
import Export from "./components/Export";
import ImageUpload from "./components/ImageUpload";
import ImageComparison from "./components/ImageComparison";
import { useState } from "react";

const API_BASE_URL = "http://localhost:5000";
//process.env.REACT_APP_BACKEND_API_URL
function App() {
  const [exportOptions, setExportOptions] = useState<{
    format: string;
    resolution: string;
  }>({
    format: "png",
    resolution: "original",
  });
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);
  const [originalImageUrl, setOriginalImageUrl] = useState<string | null>(null);
  const [processedFilename, setProcessedFilename] = useState<string | null>(null);
  const [masterFilename, setMasterFilename] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExportOptionsChange = (options: { format: string; resolution: string }) => {
    setExportOptions(options);
  };

  // Clear the selected file
  const clearFile = () => {
    setFile(null);
    if (processedImageUrl) {
      URL.revokeObjectURL(processedImageUrl);
    }
    if (originalImageUrl) {
      URL.revokeObjectURL(originalImageUrl);
    }
    setProcessedImageUrl(null);
    setOriginalImageUrl(null);
    setProcessedFilename(null);
    setMasterFilename(null);
    setError(null);
  };

  // Handle file upload and set preview
  const handleFileUpload = (file: File) => {
    const imageUrl = URL.createObjectURL(file);
    setOriginalImageUrl(imageUrl);
    setFile(file);
    setProcessedImageUrl(null);
    setProcessedFilename(null);
    setMasterFilename(null);
    setError(null);
  };

  // Remove background using API
  const handleRemoveBg = async () => {
    if (!file) {
      setError("Please select an image.");
      return;
    }
    setProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/api/remove-background`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Background removal failed");
      }

      const result = await response.json();
      setMasterFilename(result.master_file);

      // Set the processed image URL for preview (using master)
      const masterUrl = `${API_BASE_URL}/api/download/${result.master_file}`;
      setProcessedImageUrl(masterUrl);
    } catch (err: unknown) {
      console.error("Background removal failed:", err);
      setError("Background removal failed. Please try again.");
    }
    setProcessing(false);
  };

  // Download the processed image
  const handleDownloadImage = async () => {
    if (!masterFilename) {
      setError("Please process an image first.");
      return;
    }
    setProcessing(true);

    try {
      // Step 2: Prepare the download with selected options
      const formData = new FormData();
      formData.append("master_file", masterFilename);
      formData.append("resolution", exportOptions.resolution);
      formData.append("format", exportOptions.format);

      const prepareResponse = await fetch(`${API_BASE_URL}/api/prepare-download`, {
        method: "POST",
        body: formData,
      });

      if (!prepareResponse.ok) {
        throw new Error("Failed to prepare image for download");
      }

      const { output_file } = await prepareResponse.json();
      
      // Step 3: Trigger the actual download
      const downloadUrl = `${API_BASE_URL}/api/download/${output_file}`;
      const link = document.createElement("a");
      link.href = downloadUrl;
      
      const ext = exportOptions.format.toLowerCase();
      link.download = `processed_image_${exportOptions.resolution}.${ext}`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error("Error downloading image:", err);
      setError("Failed to download the image. Please try again.");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="logo-container">
          <img
            src="/imgPixel.png"
            alt="ImgPixel Logo"
            className="logo-image"
          />
          <div className="logo-text-container">
            <h1 className="logo-text-green">Img</h1>
            <h1 className="logo-text-white">Pixel</h1>
          </div>
        </div>
        <p className="tagline">Remove backgrounds with AI • Fast & Free</p>
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Left Panel - Controls */}
        <aside className="left-panel">
          <div className="control-section">
            <ImageUpload
              file={file}
              setFile={(fileOrNull) => {
                if (fileOrNull) {
                  handleFileUpload(fileOrNull);
                } else {
                  clearFile();
                }
              }}
              processing={processing}
              clearFile={clearFile}
              handleRemoveBg={handleRemoveBg}
              error={error}
            />
          </div>

          <div className="control-section">
            <Export
              onExportOptionsChange={handleExportOptionsChange}
              onDownloadImage={handleDownloadImage}
              exportOptions={exportOptions}
              disabled={!processedImageUrl}
            />
          </div>
        </aside>

        {/* Right Panel - Preview */}
        <main className="right-panel">
          <div className="preview-container">
            <ImageComparison
              originalImage={originalImageUrl}
              processedImage={processedImageUrl}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
