from app.db.session import engine
from app.db.base import Base

# importa os models para que o SQLAlchemy registre as tabelas
from app.db.models.user import User
from app.db.models.ticket import Ticket
from app.db.models.comment import Comment


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
