from flask_scenario_testing.support.Time import Time


class ScenarioConfig(object):
    def __init__(self, _id: str, users_count: int, run_time: str, modifiers, options: dict, meta: dict):
        self._users_count = users_count
        self._run_time = run_time
        self._modifiers = modifiers
        self._id = _id
        self._options = options
        self._meta = meta

    def meta(self) -> dict:
        return self._meta

    def users_count(self):
        return self._users_count

    def run_time(self) -> Time:
        return Time.from_string(self._run_time)

    def modifiers(self):
        return self._modifiers

    def id(self):
        return self._id

    def options(self):
        return self._options
