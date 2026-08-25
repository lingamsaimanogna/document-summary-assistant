import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [summaryLength, setSummaryLength] = useState("medium");
  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [extractedText, setExtractedText] = useState("");
  const [loading, setLoading] = useState(false);

  const allowedTypes = [
    "application/pdf",
    "image/png",
    "image/jpeg"
  ];

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    if (!allowedTypes.includes(selectedFile.type)) {
      setFile(null);
      setPopupMessage(
        "Please upload a PDF, PNG, JPG or JPEG file."
      );
      setShowPopup(true);
      return;
    }

    setFile(selectedFile);
    setExtractedText("");
  };

  const handleFileChange = (event) => {
    handleFile(event.target.files[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    handleFile(event.dataTransfer.files[0]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleSummarize = async () => {
    if (!file) {
      setPopupMessage("Please select a document first.");
      setShowPopup(true);
      return;
    }
    setLoading(true);
    setExtractedText("");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("summary_length", summaryLength);
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/summarize`,
        formData
      );
      setExtractedText(response.data.result);
    } catch (error) { 
      const message =
        error.response?.data?.detail ||
        "Unable to generate summary.";
      setPopupMessage(message);
      setShowPopup(true);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="app">
      <div className="container">

        <h1>Document Summary Assistant</h1>

        <p className="subtitle">
          Upload a PDF or image and generate an intelligent summary
        </p>

        <div
          className="upload-box"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="upload-icon">📄</div>

          <h2>Upload your document</h2>

          <p>Drag and drop your file here</p>
          <p>or</p>

          <label className="upload-button">
            Choose File
            <input
              type="file"
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={handleFileChange}
              hidden
            />
          </label>

          <p className="file-types">
            Supported formats: PDF, PNG, JPG, JPEG
          </p>

          {file && (
            <div className="file-info">
              <strong>Selected file:</strong>
              <br />
              {file.name}
            </div>
          )}
        </div>

        <div className="summary-section">

          <h2>Summary Length</h2>

          <div className="length-options">

            <button
              className={summaryLength === "short" ? "active" : ""}
              onClick={() => setSummaryLength("short")}
            >
              Short
            </button>

            <button
              className={summaryLength === "medium" ? "active" : ""}
              onClick={() => setSummaryLength("medium")}
            >
              Medium
            </button>

            <button
              className={summaryLength === "long" ? "active" : ""}
              onClick={() => setSummaryLength("long")}
            >
              Long
            </button>

          </div>

          <button
            className="summarize-button"
            disabled={!file || loading}
            onClick={handleSummarize}
          >
            {loading ? "Generating Summary..." : "Summarize Document"}
          </button>
          {loading && (
            <p className="loading-message">
              Extracting text and generating your summary...
            </p>
          )}
        </div>
        {extractedText && (
          <div className="result-section">
            <h2>Generated Summary</h2>

            <div className="text-box">
              {extractedText}
            </div>
          </div>
        )}

        {showPopup && (
          <div className="popup-overlay">
            <div className="popup">

              <div className="popup-icon">⚠️</div>

              <h2>Notice</h2>

              <p>{popupMessage}</p>

              <button
                onClick={() => setShowPopup(false)}
                className="popup-button"
              >
                OK
              </button>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;