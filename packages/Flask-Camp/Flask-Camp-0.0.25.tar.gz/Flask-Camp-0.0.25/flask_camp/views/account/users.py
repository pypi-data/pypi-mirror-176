from flask import request, current_app
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from flask_camp._schemas import schema
from flask_camp._utils import current_api
from flask_camp._services._security import allow
from flask_camp.models._user import User

rule = "/users"


@allow("moderator")
def get():
    """Get a list of users"""

    limit = request.args.get("limit", default=30, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if not 0 <= limit <= 100:
        raise BadRequest("Limit can't be lower than 0 or higher than 100")

    query = User.query

    users = query.order_by(User.id.desc()).limit(limit).offset(offset)

    return {"status": "ok", "users": [user.as_dict() for user in users], "count": query.count()}


@allow("anonymous", "authenticated")
@schema("create_user.json")
def post():
    """Create an user"""

    if current_user.is_authenticated:
        raise BadRequest()

    data = request.get_json()["user"]

    current_api.validate_user_schema(data)

    try:
        user = User.create(
            name=data["name"],
            password=data["password"],
            email=data["email"],
            data=data.get("data"),
        )
        current_api.database.session.add(user)
        current_api.database.session.flush()
        current_api.before_create_user.fire(user=user)
        current_api.database.session.commit()
    except IntegrityError as e:
        raise BadRequest("A user still exists with this name") from e

    try:
        user.send_account_creation_mail()
    except:  # pylint: disable=bare-except
        current_app.logger.exception("Fail to send mail", exc_info=True)

    return {"status": "ok", "user": user.as_dict()}
