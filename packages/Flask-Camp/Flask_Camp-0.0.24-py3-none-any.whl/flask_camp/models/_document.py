from __future__ import annotations

import json

from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, reconstructor
from sqlalchemy.sql import func
from werkzeug.exceptions import BadRequest

from flask_camp._utils import current_api
from flask_camp.models._base_model import BaseModel
from flask_camp.models._user import User
from flask_camp.models._tag import Tag


def _as_dict(document, version, include_hidden_data_for_staff=False):

    if document.is_redirection:
        return {"id": document.id, "redirects_to": document.redirects_to}

    result = {
        "id": document.id,
        "protected": document.protected,
        "comment": version.comment,
        "hidden": version.hidden,
        "timestamp": None if version.timestamp is None else version.timestamp.isoformat(),
        "user": None if version.user is None else version.user.as_dict(),
        "last_version_id": document.last_version_id,
        "version_id": version.id,
    }

    if not version.hidden:
        result["data"] = version.data
    elif include_hidden_data_for_staff and (current_user.is_admin or current_user.is_moderator):
        result["data"] = version.data

    return result


class Document(BaseModel):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)

    protected = Column(Boolean, nullable=False, default=False)

    tags = relationship(Tag, back_populates="document", lazy="select", cascade="all,delete")

    versions = relationship(
        lambda: DocumentVersion,
        primaryjoin=lambda: Document.id == DocumentVersion.document_id,
        backref="document",
        lazy="select",
        cascade="all,delete,delete-orphan",
    )

    last_version_id = Column(Integer, ForeignKey("version.id", use_alter=True))
    last_version = relationship(
        lambda: DocumentVersion,
        primaryjoin=lambda: Document.last_version_id == DocumentVersion.id,
        uselist=False,
        single_parent=True,
        post_update=True,
    )

    redirects_to = Column(Integer, ForeignKey("document.id"), index=True)

    associated_ids = Column(ARRAY(Integer), index=True)

    @classmethod
    def create(cls, comment, data, author=None):

        result = cls()

        version = DocumentVersion(
            document=result,
            user=current_user if author is None else author,
            comment=comment,
            data=data,
        )

        result.last_version = version
        result.associated_ids = current_api.get_associated_ids(version.as_dict())

        current_api.database.session.add(result)
        current_api.database.session.add(version)
        current_api.database.session.flush()

        return result

    def update_last_version_id(self):
        """call this when a version has been hidden or deleted"""
        query = DocumentVersion.query

        query = query.filter_by(document_id=self.id).order_by(DocumentVersion.id.desc())
        self.last_version = query.first()

        if self.last_version is None:
            raise BadRequest("There is no visible version associated with this document")

        if self.last_version.hidden:
            raise BadRequest("The last version of a document cannot be hidden")

        self.last_version_id = self.last_version.id

    def clear_memory_cache(self):
        current_api.memory_cache.delete_document(self.id)

        query = select(Document.id).where(Document.associated_ids.contains([self.id]))
        for row in current_api.database.session.execute(query):
            current_api.memory_cache.delete_document(row[0])

    def as_dict(self):
        return _as_dict(self, self.last_version)

    @property
    def is_redirection(self):
        return self.redirects_to is not None

    @classmethod
    def get(cls, with_for_update=False, **kwargs) -> Document:
        return super(Document, cls).get(with_for_update=with_for_update, **kwargs)


class DocumentVersion(BaseModel):
    __tablename__ = "version"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("document.id"), index=True)

    user_id = Column(Integer, ForeignKey(User.id), index=True)
    user = relationship(User)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(String)

    hidden = Column(Boolean, default=False, nullable=False)
    _data = Column("data", String)

    tags = relationship(
        "Tag",
        lazy="select",
        foreign_keys="DocumentVersion.document_id",
        primaryjoin=document_id == Tag.document_id,
        uselist=True,
        viewonly=True,
    )

    def __init__(self, data, **kwargs):
        super().__init__(_data=json.dumps(data), **kwargs)
        self._init_from_database()

    @reconstructor
    def _init_from_database(self):
        self._raw_data = json.loads(self._data)

    def as_dict(self):
        return _as_dict(self.document, self, include_hidden_data_for_staff=True)

    @property
    def data(self):
        return self._raw_data

    @data.setter
    def data(self, value):
        self._raw_data = value
        self._data = json.dumps(value)

    @classmethod
    def get(cls, with_for_update=False, **kwargs) -> DocumentVersion:
        return super(DocumentVersion, cls).get(with_for_update=with_for_update, **kwargs)
