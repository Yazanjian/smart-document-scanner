from typing import Union

from pydantic import BaseModel

from app.models.documents import Document


class OCRResponse(BaseModel):
    name: str
    document: Union[Document, None]
