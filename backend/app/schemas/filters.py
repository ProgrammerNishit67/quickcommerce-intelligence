from typing import Optional
from pydantic import BaseModel

class FilterParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    store_id: Optional[str] = None
    category: Optional[str] = None
