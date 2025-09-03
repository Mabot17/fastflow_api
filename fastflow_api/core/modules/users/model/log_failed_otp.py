from database import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Text


class LogFailedOTPModel(Base):
    __tablename__ = "log_failed_otp"

    id = Column("faotp_id", BigInteger, primary_key=True, index=True)
    user_id = Column("faotp_user_id", BigInteger)
    tested_otp = Column("faotp_tested_otp", String(45))
    valid_otp = Column("faotp_valid_otp", String(45))
    notes = Column("faotp_notes", Text)
    created_by = Column("faotp_created_by", String(100))
    updated_by = Column("faotp_updated_by", String(100))
    deleted_by = Column("faotp_deleted_by", String(100))
    created_at = Column("faotp_created_at", DateTime)
    updated_at = Column("faotp_updated_at", DateTime)
    deleted_at = Column("faotp_deleted_at", DateTime)
