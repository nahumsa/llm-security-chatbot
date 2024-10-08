from typing import Generator
from common.config import PostgresSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from database.model import Base


pg_settings = PostgresSettings()  # type: ignore
engine = create_engine(pg_settings.pg_conn_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    db_session = SessionLocal()
    try:
        yield db_session

    finally:
        db_session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
