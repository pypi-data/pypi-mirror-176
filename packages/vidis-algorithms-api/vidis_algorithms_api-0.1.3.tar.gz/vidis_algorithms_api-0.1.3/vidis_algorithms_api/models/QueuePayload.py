from typing import Any, Dict, Optional

from pydantic import BaseModel


class Payload(BaseModel):
    task_id: str
    specter_id: str
    name: str
    path: str
    params: Optional[Dict[Any, Any]]
