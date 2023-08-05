from typing import Any, Dict, Optional

from pydantic import BaseModel


class Payload(BaseModel):
    id: str
    specter_id: str
    name: str
    path: str
    params: Optional[Dict[Any, Any]]
