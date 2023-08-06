from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class TargetAPI(BaseModel):
    url: str
    method: str
    header: Optional[Dict]
    parameters: Optional[Dict]
    save_response: bool = False


class ConfigModel(BaseModel):
    name: str
    description: str
    config: Dict[str, TargetAPI]


class ProxyModel(BaseModel):
    http_proxy: str
    https_proxy: str
    no_proxy: str


class RequestResponse(BaseModel):
    success: bool = False
    data: Any = None
    code: int = 0
    message: Optional[str]