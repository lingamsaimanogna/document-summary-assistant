# Document Summary Assistant
A simple web application that takes a PDF or image document and generates a summary using AI.

## What it does
* Upload PDF, PNG, JPG or JPEG files
* Supports drag and drop
* Extracts text from PDFs
* Uses OCR for images and scanned documents
* Generates short, medium or long summaries
* Shows important key points
* Shows loading and error messages

## Tech Used
**Frontend**
* React
* Vite
* Axios
* CSS

**Backend**
* Python
* FastAPI
* Uvicorn

**Other**
* PyMuPDF for PDF text extraction
* Tesseract OCR for images
* Pillow for image processing
* Google Gemini API for summarization

## How it works
<img width="120" height="218" alt="image" src="https://github.com/user-attachments/assets/06a75783-c8cb-4a52-a883-9b419cff577f" />


## Project Structure
<img width="150" height="228" alt="image" src="https://github.com/user-attachments/assets/2b9e55aa-ebdd-45be-a24f-1498d0a55f2e" />


## How to Run
### Requirements
Make sure you have:
* Python 3.x
* Node.js and npm
* Tesseract OCR

### Backend
Open a terminal and go to the backend folder:
-> cd backend

Create a virtual environment:
-> python -m venv venv

Activate it on Windows:
-> .\venv\Scripts\Activate.ps1

Install the required packages:
-> pip install -r requirements.txt

Create a `.env` file inside the `backend` folder:
-> GEMINI_API_KEY=your_api_key_here

Then start the backend:
-> python -m uvicorn main:app --reload

Backend:
http://127.0.0.1:8000

FastAPI docs:
http://127.0.0.1:8000/docs

### Frontend
Open another terminal and go to the frontend folder:
-> cd frontend

Install the packages:
-> npm install

Start the frontend:
-> npm run dev

Open the application at:
http://localhost:5173

### Running both
Keep the backend running in one terminal and the frontend running in another.

**Terminal 1:**

cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload

**Terminal 2:**

cd frontend
npm run dev


## Notes
The Gemini API key is stored in `.env` and should not be uploaded to GitHub.
The application currently processes one document at a time.

## Future Improvements
* Better formatting of generated summaries
* Download summary option
* Document history
* Support for larger documents
* Improved OCR for low-quality scans
