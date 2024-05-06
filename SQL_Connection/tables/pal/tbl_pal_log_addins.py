from datetime import datetime
from uuid import UUID  # , uuid4

from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Uuid,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from APICore.result_models.pal.doc_sessions import PALLogAddIn
from SQL_Connection.db_connection import Base, NotFoundError, SessionLocal


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblPALLogAddIns(Base):
    __tablename__ = "logAddIns"
    __table_args__ = {"schema": "pal"}

    id: Mapped[UUID] = mapped_column(
        Uuid(), primary_key=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    docSessionId: Mapped[UUID] = mapped_column(
        ForeignKey("pal.docSessions.id"), nullable=False
    )
    logDate: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    uploadedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    refreshedId: Mapped[UUID] = mapped_column(
        ForeignKey("core.refreshed.id"), nullable=False
    )


## function to write to create a new entry item in the table
def create_new_log_addin(
    item: PALLogAddIn,
    refreshed,
    session: Session = None,
) -> PALLogAddIn:
    base_item = PALLogAddIn(**item.model_dump(exclude_none=True))
    new_entry = TblPALLogAddIns(
        **base_item.model_dump(exclude_none=True), refreshedId=refreshed.id
    )
    if session is None:
        db = SessionLocal()
        try:
            new_entry = read_db_log_addin(item, db)
        except NotFoundError:
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)
        finally:
            db.close()
    else:
        try:
            new_entry = read_db_log_addin(item, session)
        except NotFoundError:
            session.add(new_entry)
            session.commit()
            session.refresh(new_entry)
    return new_entry


## function to read item from the table
def read_db_log_addin(item: PALLogAddIn, session: Session) -> PALLogAddIn:
    db_item = (
        session.query(TblPALLogAddIns).filter(TblPALLogAddIns.id == item.id).first()
    )
    if db_item is None:
        raise NotFoundError(f"LogAddInId: {item.id} not found")
    db_item_dump = {}
    for key, value in db_item.__dict__.items():
        db_item_dump.update({key: value})
    return PALLogAddIn(**db_item_dump)


## function to update the table
def update_log_addin():
    pass


## function to delete item from the table
def delete_log_addin():
    pass
