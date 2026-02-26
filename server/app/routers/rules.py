import json
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, select
from ..models import Rule

router = APIRouter(prefix='/api/rules', tags=['rules'])


class RulePayload(BaseModel):
    name: str
    enabled: bool = True
    camera_id_optional: str | None = None
    conditions: dict
    actions: dict


@router.get('')
def list_rules(request: Request):
    with Session(request.app.state.db_engine) as session:
        return session.exec(select(Rule)).all()


@router.post('')
def create_rule(payload: RulePayload, request: Request):
    with Session(request.app.state.db_engine) as session:
        rule = Rule(
            name=payload.name,
            enabled=payload.enabled,
            camera_id_optional=payload.camera_id_optional,
            conditions_json=json.dumps(payload.conditions),
            actions_json=json.dumps(payload.actions),
        )
        session.add(rule)
        session.commit()
        session.refresh(rule)
        return rule


@router.delete('/{rule_id}')
def delete_rule(rule_id: int, request: Request):
    with Session(request.app.state.db_engine) as session:
        rule = session.get(Rule, rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail='rule not found')
        session.delete(rule)
        session.commit()
    return {'status': 'deleted'}
