from flask import request
from flask_login import current_user
from werkzeug.exceptions import BadRequest, NotFound

from flask_camp._schemas import schema
from flask_camp._services._security import allow
from flask_camp._utils import current_api, JsonResponse
from flask_camp.models._tag import Tag

rule = "/tags"


def _build_filters(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


@allow("anonymous", "authenticated", allow_blocked=True)
def get():
    """Get user tag list"""
    limit = request.args.get("limit", default=100, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if not 0 <= limit <= 100:
        raise BadRequest("Limit can't be lower than 0 or higher than 100")

    filters = _build_filters(
        user_id=request.args.get("user_id", default=None, type=int),
        document_id=request.args.get("document_id", default=None, type=int),
        name=request.args.get("name", default=None, type=str),
        value=request.args.get("value", default=None, type=str),
    )

    query = Tag.query

    if len(filters) != 0:
        query = query.filter_by(**filters)

    count = query.count()
    query = query.order_by(Tag.id).offset(offset).limit(limit)

    return JsonResponse(
        {
            "status": "ok",
            "count": count,
            "tags": [tag.as_dict() for tag in query],
        }
    )


@allow("authenticated", allow_blocked=True)
@schema("modify_tag.json")
def post():
    """create/modify an user tag"""
    data = request.get_json()

    document_id = data["document_id"]
    name = data["name"]
    value = data.get("value", None)

    tag = Tag.get(name=name, document_id=document_id, user_id=current_user.id)
    if tag is None:
        tag = Tag(name=name, document_id=document_id, user_id=current_user.id)
        current_api.database.session.add(tag)

    tag.value = value

    current_api.database.session.commit()

    return JsonResponse({"status": "ok", "tag": tag.as_dict()})


@allow("authenticated", allow_blocked=True)
@schema("delete_tag.json")
def delete():
    """Delete an user tag"""
    data = request.get_json()

    document_id = data["document_id"]
    name = data["name"]

    tag = Tag.get(name=name, document_id=document_id, user_id=current_user.id)

    if not tag:
        raise NotFound()

    current_api.database.session.delete(tag)
    current_api.database.session.commit()

    return JsonResponse({"status": "ok"})
