import uuid
from datetime import datetime, timedelta, UTC


class Session:
    def __init__(self):
        self.sessions = {}
        self.__expires = 30

    @staticmethod
    def format_date(date: datetime):
        return date.strftime('%a, %d-%b-%Y %H:%M:%S UTC')

    def set_cookie(self, cookies: list) -> dict | str:
        cookie_dict = {}
        for cookie in cookies:
            if not cookie:
                continue
            name, value = cookie.split('=', 1)
            cookie_dict[name.strip()] = value.strip()
        session_id = cookie_dict.get('session')
        if not session_id or session_id not in self.sessions.keys():
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {'expires': self.expires()}
            return f'session={session_id}; expires={self.format_date(self.sessions[session_id]['expires'])}'
        return self.sessions[session_id]

    def expires(self) -> datetime:
        return datetime.now(UTC) + timedelta(days=self.__expires)


session = Session()
