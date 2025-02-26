from sqlalchemy.orm import Mapped, DeclarativeBase, relationship, mapped_column
from sqlalchemy import (
    func,
    String,
    Integer,
    BigInteger,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    Text,
    Boolean,
    Numeric,
    Table,
    Date,
    select,
    DECIMAL, Column,
)


class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    send: Mapped[bool] = mapped_column(default=True)


class Domain(Base):
    __tablename__ = "domains"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column()
    banned: Mapped[bool] = mapped_column(default=False)