import json
from datetime import datetime
from sqlmodel import Session, select
from ..models import Event, EventTag, Notification, Rule


class RuleEngine:
    def apply(self, session: Session, event: Event, tags: list[str]) -> None:
        rules = session.exec(select(Rule).where(Rule.enabled == True)).all()  # noqa: E712
        for rule in rules:
            conditions = json.loads(rule.conditions_json or '{}')
            actions = json.loads(rule.actions_json or '{}')
            if not self._matches(rule, conditions, event, tags):
                continue
            if actions.get('mark_important'):
                event.important = True
            if actions.get('create_notification'):
                session.add(Notification(title=f'Rule: {rule.name}', body=f'Event {event.id} matched rule {rule.name}', channel='web'))
            for tag in actions.get('add_tags', []):
                session.add(EventTag(event_id=event.id, tag=tag, confidence=0.8, source='rule'))

    def _matches(self, rule: Rule, conditions: dict, event: Event, tags: list[str]) -> bool:
        if rule.camera_id_optional and rule.camera_id_optional != event.camera_id:
            return False
        if conditions.get('time_window') == 'night':
            hour = event.created_at.hour
            if 6 <= hour <= 20:
                return False
        tag_match = conditions.get('tag_match')
        if tag_match and tag_match not in tags:
            return False
        cam = conditions.get('camera_match')
        if cam and cam != event.camera_id:
            return False
        return True
