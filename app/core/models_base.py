from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy import Column

@declarative_mixin
class TimestampMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
