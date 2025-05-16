# Smart Document Scanner - VLM Approach

This project allows you to extract useful data from **PDFs** or **images** using **LLMs (Large Language Models)**. With the power of **GPT-4o**, it can read visual inputs (images or PDFs), extract text, and structure it into a **JSON response** useful for your application.

---

## Features

- **Vision-based Extraction**: Upload a PDF or image and extract raw text and structured data using OpenAI's GPT-4o.
- **LLM Structuring**: Use GPT-4o or any other LLM to process the extracted text and structure it into a meaningful JSON response.
- **API-based**: The system exposes a single API endpoint, `/ocr`, where you can upload documents or images and retrieve the extracted data.
- **Configurable Translation Support**: You can choose your preferred language and whether to translate the extracted data.

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

1. **Poppler (for PDF support via pdf2image)**

   - **Windows**: Download from [http://blog.alivate.com.au/poppler-windows/](http://blog.alivate.com.au/poppler-windows/) and add the `bin/` folder to your PATH.
   - **Linux**: `sudo apt install poppler-utils`
   - **macOS**: `brew install poppler`

2. **Python Dependencies**

   - Install required libraries by creating a venv then run:

     ```bash
     pip install -r requirements.txt
     ```

---

## Configuration

This project uses a `.env` file for environment-based configuration.

Create a `.env` file in the project root and define the following keys:

```env
# Text-only LLM model to use (e.g., gpt-3.5-turbo, gpt-4, etc.)
TEXT_MODEL_NAME=gpt-3.5-turbo

# Vision-capable model (e.g., gpt-4o)
VISION_MODEL_NAME=gpt-4o

# OpenAI API Key (or other LLM provider’s key)
OPENAI_API_KEY=your_openai_api_key_here

# ======= OPTIONAL: =======

# Text-only LLM Temperature
TEXT_MODEL_TEMPERATURE=0

# Vision-capable LLM Temperature
VISION_MODEL_TEMPERATURE=0

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

## MIT License

Copyright (c) 2025 Yazan Jian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
