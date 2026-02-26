from collections.abc import Generator
from sqlmodel import Session, SQLModel, create_engine


def build_engine(db_url: str):
    return create_engine(db_url, connect_args={'check_same_thread': False})


def init_db(engine) -> None:
    SQLModel.metadata.create_all(engine)


def get_session_from_engine(engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
