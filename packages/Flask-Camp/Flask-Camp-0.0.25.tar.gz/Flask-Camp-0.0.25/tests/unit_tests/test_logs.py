from tests.unit_tests.utils import BaseTest


def _assert_log(log, action, user, document_id=None, version_id=None, target_user_id=None, comment=None):

    assert log["action"] == action
    assert log["user"]["id"] == user.id
    assert log["document_id"] == document_id
    assert log["version_id"] == version_id
    assert log["target_user_id"] == target_user_id
    assert log["comment"] == comment


class Test_Logs(BaseTest):
    rest_api_kwargs = {"user_roles": "bot,contributor"}

    def test_anonymous_get(self):
        self.get_logs()

    def test_hide_version(self, moderator):
        self.login_user(moderator)

        doc = self.create_document().json["document"]
        self.modify_document(doc, data="v2")

        self.hide_version(doc)
        self.unhide_version(doc)

        r = self.get_logs()
        assert r.json["count"] == 2, r.json

        logs = r.json["logs"]

        assert logs[-1]["action"] == "hide_version"
        assert logs[-1]["version_id"] == doc["version_id"]
        assert logs[-1]["document_id"] == doc["id"]
        assert logs[-1]["user"]["id"] == moderator.id
        assert logs[-2]["action"] == "unhide_version"
        assert logs[-2]["version_id"] == doc["version_id"]
        assert logs[-2]["document_id"] == doc["id"]
        assert logs[-2]["user"]["id"] == moderator.id

    def test_errors(self):
        self.get_logs(limit=101, expected_status=400)

    def test_typical_scenario(self, user, moderator, admin):

        self.login_user(moderator)
        self.block_user(user, comment="vandal!")
        self.unblock_user(user, comment="mistake")

        doc = self.create_document().json["document"]
        doc_v2 = self.modify_document(doc, data="v2").json["document"]
        self.modify_document(doc_v2, data="v3")

        self.protect_document(doc, comment="needs protection")
        self.unprotect_document(doc, comment="ok!")

        self.logout_user()
        self.login_user(admin)

        self.modify_user(user, roles=["moderator"], comment="he's worthy")
        self.modify_user(user, roles=[], comment="nope")
        self.modify_user(user, roles=["admin"], comment="maybe god")
        self.modify_user(user, roles=["admin", "bot"], comment="or bot")
        self.modify_user(user, roles=["bot"], comment="not even close")
        self.modify_user(user, roles=[], comment="he's an human")

        self.delete_version(doc_v2, comment="crap!")
        self.delete_document(doc, comment="Total crap")

        result = self.get_logs().json
        assert result["count"] == 12, result

        logs = result["logs"]

        _assert_log(logs[-1], "block", moderator, target_user_id=user.id, comment="vandal!")
        _assert_log(logs[-2], "unblock", moderator, target_user_id=user.id, comment="mistake")

        _assert_log(logs[-3], "protect", moderator, document_id=doc["id"], comment="needs protection")
        _assert_log(logs[-4], "unprotect", moderator, document_id=doc["id"], comment="ok!")

        _assert_log(logs[-5], "add_role moderator", admin, target_user_id=user.id, comment="he's worthy")
        _assert_log(logs[-6], "remove_role moderator", admin, target_user_id=user.id, comment="nope")

        _assert_log(logs[-7], "add_role admin", admin, target_user_id=user.id, comment="maybe god")
        _assert_log(logs[-8], "add_role bot", admin, target_user_id=user.id, comment="or bot")

        _assert_log(logs[-9], "remove_role admin", admin, target_user_id=user.id, comment="not even close")
        _assert_log(logs[-10], "remove_role bot", admin, target_user_id=user.id, comment="he's an human")

        _assert_log(
            logs[-11], "delete_version", admin, document_id=doc["id"], version_id=doc_v2["version_id"], comment="crap!"
        )
        _assert_log(logs[-12], "delete_document", admin, document_id=doc["id"], comment="Total crap")
