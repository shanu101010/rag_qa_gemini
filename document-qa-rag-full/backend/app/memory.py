from collections import deque
from .config import SHORT_TERM_WINDOW

sessions = {}

def add_to_session(session_id: str, query: str, answer: str):
    dq = sessions.get(session_id)
    if dq is None:
        dq = deque(maxlen=SHORT_TERM_WINDOW)
        sessions[session_id] = dq
    dq.append((query, answer))

def get_session_context(session_id: str):
    dq = sessions.get(session_id, deque())
    return list(dq)
