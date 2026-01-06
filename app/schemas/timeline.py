from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


class TimelineItem(BaseModel):
    type: Literal["event", "comment"]
    created_at: datetime

    # event
    event_type: Optional[str] = None
    from_status: Optional[str] = None
    to_status: Optional[str] = None

    # comment
    content: Optional[str] = None

    user_id: int
