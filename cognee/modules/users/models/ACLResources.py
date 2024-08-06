from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, UUID, DateTime
from cognee.infrastructure.databases.relational import Base

class ACLResources(Base):
    __tablename__ = "acl_resources"

    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))

    acl_id = Column(UUID(as_uuid = True), ForeignKey("acls.id"), primary_key = True)
    resource_id = Column(UUID(as_uuid = True), ForeignKey("resources.id"), primary_key = True)
