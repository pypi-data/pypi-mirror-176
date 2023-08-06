from copy import deepcopy
import json

from flask_camp.models import User

from tests.unit_tests.utils import BaseTest


class Test_Document(BaseTest):
    def assert_document(self, document, user: User, data, comment="creation"):
        self.assert_document_schema(document)

        assert document["comment"] == comment
        assert json.dumps(document["data"]) == json.dumps(data)

        assert document["user"]["id"] == user.id
        assert document["user"]["name"] == user.name
        assert document["user"]["blocked"] == user.blocked

    def test_errors(self, user):
        self.create_document(expected_status=403)  # not logged

        self.login_user(user)

        fake_doc = {"id": 42, "version_id": 1, "data": None}

        self.get_document(fake_doc, expected_status=404)
        self.modify_document(fake_doc, expected_status=404)

        r = self.post("/documents", json={"comment": "xxx", "document": {"namespace": "x"}}, expected_status=400)
        assert r.json["description"] == "'data' is a required property on instance ['document']"

        r = self.post("/documents", json={"document": {"namespace": "x", "data": "x"}}, expected_status=400)
        assert r.json["description"] == "'comment' is a required property on instance "

    def test_creation(self, user):
        self.login_user(user)

        r = self.create_document(data={"value": "42"}, comment="XXX")
        self.assert_document(r.json["document"], user, data={"value": "42"}, comment="XXX")

        document_id = r.json["document"]["id"]

        r = self.get_document(document_id)
        self.assert_document(r.json["document"], user, data={"value": "42"}, comment="XXX")
        assert r.json["document"]["version_id"] == r.json["document"]["last_version_id"]

    def test_modification(self, user):
        self.login_user(user)

        v1 = self.create_document(expected_status=200).json["document"]
        v2 = self.modify_document(v1, comment="test", data={"value": "43"}, expected_status=200).json["document"]

        self.assert_document(v2, user, comment="test", data={"value": "43"})

        r = self.get_document(v1)
        assert r.json["document"]["version_id"] == r.json["document"]["last_version_id"]

        r = self.get_documents()
        assert r.json["status"] == "ok"
        assert r.json["count"] == 1
        assert r.json["documents"][0]["version_id"] == v2["version_id"]

    def test_modification_error(self, user):
        self.login_user(user)

        doc = self.create_document(expected_status=200).json["document"]
        payload = deepcopy(doc)
        payload["id"] = 999

        r = self.post(f"/document/{doc['id']}", json={"comment": "test", "document": payload}, expected_status=400).json
        assert r["description"] == "Id in body does not match id in URI"

        payload = deepcopy(doc)
        payload["id"] = None

        r = self.post(f"/document/{doc['id']}", json={"comment": "test", "document": payload}, expected_status=400).json
        assert r["description"] == "None is not of type 'integer' on instance ['document']['id']"

    def test_testing_helper(self, user):
        self.login_user(user)
        doc = self.create_document().json["document"]

        self.modify_document(doc, params={"rc_sleep": 0.01})


class Test_Delete(BaseTest):
    def test_main(self, admin):
        self.login_user(admin)
        doc = self.create_document().json["document"]
        self.delete_document(doc, expected_status=200)
        self.get_document(doc, expected_status=404)
        self.get_version(doc, expected_status=404)

    def test_deletion_error(self, user, user_2, moderator, admin):
        self.delete_document(1, expected_status=403)

        self.login_user(user)
        document = self.create_document().json["document"]
        self.delete_document(document, expected_status=403)

        self.login_user(user_2)
        self.delete_document(document, expected_status=403)

        self.login_user(moderator)
        self.delete_document(document, expected_status=403)

        self.login_user(admin)
        self.delete_document(99999, expected_status=404)
