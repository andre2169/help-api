from sqlalchemy.orm import declarative_base

Base = declarative_base()

import app.db.models
from app.db.models.user import User
from app.db.models.ticket import Ticket
from app.db.models.comment import Comment