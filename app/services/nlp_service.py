from threading import Lock
from typing import Any, Optional

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel, Field, create_model

from app.logger import logger
from app.core.config import app_settings
from app.models.documents import (
    Document,
    get_document_type_names,
    DOCUMENT_TYPE_MAP,
    DocumentTypeEnum,
)
from app.models.errors import ErrorResponse


class LlmModel:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                logger.debug("Creating new LlmModel class")
                cls._instance = super().__new__(cls)
                cls._instance._model = ChatOpenAI(
                    api_key=app_settings.openai_api_key,
                    model=app_settings.model_name,
                    temperature=app_settings.model_temperature,
                )
            return cls._instance

    @property
    def model(self):
        return self._model


class ExtractedDocumentType(BaseModel):
    type: Optional[str] = Field(..., description="The type of the document")


# Starting point
async def generate_desc_as_json(extracted_text: str) -> Any | None:
    """
    Extract the document type first to avoid injecting all the supported documents schemas in the LLM model.
    Better for scalability.
    """
    document_type = await extract_document_type(extracted_text)
    return await extract_json(extracted_text, document_type)


def build_document_model_for_type(doc_type: str):
    details_cls = DOCUMENT_TYPE_MAP.get(doc_type)
    if not details_cls:
        raise ValueError(f"Unsupported document type: {doc_type}")

    # Dynamically create a tailored Document model
    CustomDocument = create_model(
        "CustomDocument",
        type=(DocumentTypeEnum, ...),
        details=(details_cls, ...),
        __base__=Document,
    )
    return CustomDocument


async def extract_document_type(text: str) -> ErrorResponse | None | Any:
    try:
        llm_model = LlmModel()
        model = llm_model.model
        structured_model = model.with_structured_output(ExtractedDocumentType)

        supported_doc_types = get_document_type_names()

        # Prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Given the following text data, identify the document type\n"
                    "The document type must be one of the following: {supported_doc_types}\n"
                    "If the document does not meet any of the above types set the type to None\n",
                ),
                (
                    "human",
                    "Text:\n{text}\n",
                ),
            ]
        )

        chain = prompt | structured_model

        llm_output = await chain.ainvoke(
            {
                "text": text,
                "supported_doc_types": supported_doc_types,
            }
        )

        doc_type = llm_output.type

        if not doc_type:
            logger.error(f"Document Type is None ({doc_type})")
            return ErrorResponse(
                error="Missing Data",
                message="No valid type was extracted from the provided file.",
            )

        logger.debug(f"THE DOCUMENT TYPE IS: {doc_type}")
        return doc_type

    except Exception as e:
        logger.error(e)
        return None


async def extract_json(extracted_text: str, doc_type: str) -> Any | None:
    try:
        # Set up a parser
        DynamicDocument = build_document_model_for_type(doc_type)

        llm_model = LlmModel()
        model = llm_model.model
        structured_model = model.with_structured_output(DynamicDocument)

        response_language = app_settings.default_language
        enable_translation = app_settings.enable_translation

        logger.debug(f"LANGAUGE: {response_language, enable_translation}")

        # Prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Given the following text data and its type, extract the relevant details.\n"
                        "The document type is: {doc_type}\n"
                        "Dates should be formatted as YYYY-MM-DD"
                        "ALWAYS TRANSLATE THE EXTRACTED VALUES IN THE FOLLOWING LANGUAGE, LANGAUGE CODE: {language}\n"
                        if enable_translation
                        else ""
                    ),
                ),
                (
                    "human",
                    "Text:\n{text}\n",
                ),
            ]
        )

        chain = prompt | structured_model

        document = await chain.ainvoke(
            {
                "text": extracted_text,
                "language": response_language,
                "doc_type": doc_type,
            }
        )

        if not document:
            logger.error(f"Document is None ({document})")
            return ErrorResponse(
                error="Missing Data",
                message="No valid text was found in the provided document.",
            )

        logger.debug(f"THE DOCUMENT IS: {document}")
        return document

    except Exception as e:
        logger.error(e)
        return None
