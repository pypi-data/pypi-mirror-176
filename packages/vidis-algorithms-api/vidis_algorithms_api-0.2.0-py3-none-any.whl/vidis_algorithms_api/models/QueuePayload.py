from typing import Any, Dict, Optional, List

from pydantic import BaseModel


class Payload(BaseModel):
    task_id: str
    specter_id: str
    name: str
    path: str
    params: Dict[str, float]
