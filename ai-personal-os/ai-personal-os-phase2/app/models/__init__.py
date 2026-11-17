# Importing every model here makes sure SQLAlchemy knows about all tables
# before we call Base.metadata.create_all().
from app.models.conversation import Conversation, Message  # noqa: F401
from app.models.note import Note  # noqa: F401
from app.models.tag import Tag, note_tags, task_tags  # noqa: F401
from app.models.task import Task  # noqa: F401
