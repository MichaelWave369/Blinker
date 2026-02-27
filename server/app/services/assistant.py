from datetime import datetime
from sqlmodel import Session, select
from ..models import AssistantMessage, Event


class AssistantService:
    def __init__(self, engine):
        self.engine = engine

    def add_event_summary(self, event: Event) -> None:
        text = event.summary or f"Motion event on {event.camera_id} at {event.created_at.isoformat()}"
        with Session(self.engine) as session:
            session.add(AssistantMessage(role='assistant', content=text, created_at=datetime.utcnow(), source='event'))
            session.commit()

    def list_messages(self, limit: int = 100):
        with Session(self.engine) as session:
            return session.exec(select(AssistantMessage).order_by(AssistantMessage.created_at.desc()).limit(limit)).all()

    def post_user_message(self, content: str) -> AssistantMessage:
        with Session(self.engine) as session:
            user = AssistantMessage(role='user', content=content, created_at=datetime.utcnow(), source='chat')
            session.add(user)

            latest_event = session.exec(select(Event).order_by(Event.created_at.desc()).limit(1)).first()
            if latest_event and latest_event.summary:
                reply_text = f"Got it. Latest camera update: {latest_event.summary}"
            else:
                reply_text = 'Got it. No events yet—once motion is detected, I will summarize it here.'

            reply = AssistantMessage(role='assistant', content=reply_text, created_at=datetime.utcnow(), source='chat')
            session.add(reply)
            session.commit()
            session.refresh(reply)
            return reply
