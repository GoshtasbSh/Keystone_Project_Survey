import unittest

from api.guest import _filter_presence_active


class FilterPresenceActiveTests(unittest.TestCase):
    def test_keeps_only_active_user_ids(self):
        presence = [
            {"user_id": "a", "display_name": "Ann",  "last_active_at": "x"},
            {"user_id": "b", "display_name": "Bob",  "last_active_at": "y"},
            {"user_id": "c", "display_name": "Cara", "last_active_at": "z"},
        ]
        active = ["a", "c"]
        out = _filter_presence_active(presence, active)
        self.assertEqual([p["user_id"] for p in out], ["a", "c"])

    def test_empty_active_set_hides_everyone(self):
        presence = [{"user_id": "a"}, {"user_id": "b"}]
        self.assertEqual(_filter_presence_active(presence, []), [])

    def test_handles_none_inputs(self):
        self.assertEqual(_filter_presence_active(None, None), [])
        self.assertEqual(_filter_presence_active([], ["a"]), [])

    def test_drops_rows_without_user_id(self):
        presence = [{"display_name": "ghost"}, {"user_id": "a"}]
        self.assertEqual(_filter_presence_active(presence, ["a"]),
                         [{"user_id": "a"}])


if __name__ == "__main__":
    unittest.main()
