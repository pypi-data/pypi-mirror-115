from flask_scenario_testing.simulation.ScenarioConfig import ScenarioConfig
import json

from flask_scenario_testing.support.Time import Time


class ScenariosConfig(object):
    def __init__(self, scenarios: [ScenarioConfig], defaults: dict, cooldown: Time):
        self._scenarios = scenarios
        self._defaults = defaults
        self._cooldown = cooldown

    def scenarios(self) -> [ScenarioConfig]:
        return self._scenarios

    def defaults(self):
        return self._defaults

    def cooldown_time(self) -> Time:
        return self._cooldown

    @staticmethod
    def from_json(file_path: str):
        scenarios = []

        with open(file_path, 'r') as f:
            configuration = json.load(f)
            defaults = configuration.get('defaults', {})

            if configuration.get('cooldown'):
                cooldown = Time.from_string(configuration.get('cooldown'))
            else:
                cooldown = Time(0)

            for idx, dict_scenario in enumerate(configuration['scenarios']):
                scenarios.append(ScenarioConfig(
                    _id=dict_scenario.get('id', "scenario-{}".format(idx + 1)),
                    users_count=dict_scenario.get('users', defaults.get('users')),
                    run_time=dict_scenario.get('duration', defaults.get('duration')),
                    modifiers=dict_scenario.get('modifiers', defaults.get('modifiers', [])),
                    options=dict_scenario.get('options', defaults.get('options', dict())),
                    meta=dict_scenario.get('meta', defaults.get('meta', dict()))
                ))

        return ScenariosConfig(scenarios, defaults, cooldown)
