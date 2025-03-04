from sqlalchemy import text
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import SQLAlchemyError

from ..config import session_maker


def execute(query: str, params: dict = None, is_commit: bool = True) -> CursorResult:
    try:
        with session_maker() as session:
            result = session.execute(text(query), params)
            if is_commit:
                session.commit()
            return result
    except Exception as e:
        raise SQLAlchemyError(f"Error executing query: {e}") from e
