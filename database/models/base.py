from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func


Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        fields = ", ".join(f"{c.name}={getattr(self, c.name)!r}" for c in self.__table__.columns)
        return f"<{self.__class__.__name__} {fields}>"