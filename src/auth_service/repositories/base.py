from auth_service.core.database import DatabaseSession


class BaseRepository:
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session
