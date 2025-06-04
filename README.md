# Smart Document Scanner - OCR Approach

This project allows you to extract useful data from **PDFs** or **images** using **OCR (Optical Character Recognition)** and **LLMs (Large Language Models)**. The OCR functionality is powered by **Tesseract**, while the LLM is used to structure the raw data into a **JSON response** that's useful for your application.

> **Note:** If you prefer a more accurate and modern approach, consider switching to the `feature/vlm` branch. It uses **Visual Language Models (VLM)** powered by **GPT-4o**, offering significantly improved extraction quality for images and scanned documents.

---

## Features

- **OCR Extraction**: Upload a PDF or image and extract raw text data using Tesseract.
- **LLM Structuring**: Use a Large Language Model (LLM) to process the raw text and structure it into a meaningful JSON response.
- **API-based**: The system exposes a single API endpoint, `/ocr`, where you can upload documents or images and retrieve the extracted data.
- **Configurable Translation Support**: You can choose your preferred language and if you want to translate the extracted data into another language or not.

---

## API Endpoint

### `POST /ocr`

- **Description**: Upload a document or image (PDF, JPG, PNG, etc.) to extract the structured data.
- **Request**:
  - **Content-Type**: `multipart/form-data`
  - **Body**: The document or image you want to process.
  
- **Response**:
  - A JSON object containing the structured data extracted from the document/image.

---

## Prerequisites

Before running the project, choose **one of the following options**:
### Option 1: Run with Docker (Recommended)
1. Make sure you have **Docker** installed and running on your system.
2. Build the Docker image:

   ```bash
   docker build -t llm-ocr .
   ```
3. Run the container:
   ```bash
    docker run -d -p 8003:8003 -v "$(pwd)/.env:/.env" llm-ocr
   ```

### Option 2: Manual Installation

1. **Tesseract OCR**

   - **Download**: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
   - **Install**:
     - **Windows**: Run the installer. Make sure to check the box to add Tesseract to your PATH during installation.
     - **Linux**: `sudo apt install tesseract-ocr`
     - **macOS**: `brew install tesseract`
   - **Note**: After installation, you may need to **restart your IDE** so it recognizes the Tesseract path.

2. **Poppler (for PDF support via pdf2image)**

   - **Windows**: Download from [http://blog.alivate.com.au/poppler-windows/](http://blog.alivate.com.au/poppler-windows/) and add the `bin/` folder to your PATH.
   - **Linux**: `sudo apt install poppler-utils`
   - **macOS**: `brew install poppler`

3. **Python Dependencies**

   - Install required libraries by creating a venv then run:

     ```bash
     pip install -r requirements.txt
     ```

---

## Configuration

This project uses a `.env` file for environment-based configuration.

Create a `.env` file in the project root and define the following keys:

```env
# LLM model to use (e.g., gpt-3.5-turbo, gpt-4, etc.)
MODEL_NAME=gpt-3.5-turbo


# OpenAI API Key (or other LLM provider’s key)
OPENAI_API_KEY=your_openai_api_key_here

# ======= OPTIONAL: =======

# LLM Temperature
MODEL_TEMPERATURE=0

# Select the env: dev, prod
ENVIRONMENT=dev

# Language code for translation of the extracted text (e.g., en, es, fr, de)
DEFAULT_LANGUAGE=en

# Enable translation for the extracted text
ENABLE_TRANSLATION=False
```

## Insomnia Collection
For simplicity, I will add the curl for the insomnia API here, copy/paste it into insomnia to start calling the API
```commandline
curl --request POST \
  --url http://127.0.0.1:8003/api/ocr \
  --header 'Content-Type: multipart/form-data' \
  --header 'User-Agent: insomnia/11.0.0' \
  --form file=
```

## Adding Support for New Document Types

To support a new document type (e.g., contract, medical report, certificate  etc.), you only need to follow a single step:

1. **Define a Pydantic Model**  
   Add a new `Pydantic` class that represents the structure of your new document type inside the file:

```python
app/models/documents.py
```

**Example:**
```python
class MyNewDocumentType(DocumentDetails):
    field1: Optional[str] = Field(None, description="your description goes here")
    field2: Optional[str] = Field(None, description="your description goes here")
    # Add more fields as needed
```
