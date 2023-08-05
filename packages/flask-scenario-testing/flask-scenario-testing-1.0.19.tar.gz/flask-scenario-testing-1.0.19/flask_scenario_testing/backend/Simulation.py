from datetime import datetime
from typing import Optional, List
import random


class RunningScenario(object):

    def __init__(self, name: str, started_at: datetime, modifiers: dict, options: dict):
        self._name = name
        self._started_at = started_at
        self._modifiers = modifiers
        self._stopped_at = None
        self._options = options

    def name(self) -> str:
        return self._name

    def options(self) -> dict:
        return self._options

    def started_at(self) -> datetime:
        return self._started_at

    def ended_at(self) -> datetime:
        return self._stopped_at

    def has_modifiers(self):
        return bool(self._modifiers)

    def modifiers(self):
        return self._modifiers

    def end(self):
        self._stopped_at = datetime.utcnow()

    def is_running(self):
        return self._stopped_at is None


class Simulation:
    """
        Keeps track of running scenarios.
    """

    def __init__(self):
        self._scenarios = []
        self._started_at = None
        self._stopped_at = None

    def started_at(self):
        return self._started_at

    def stopped_at(self):
        return self._stopped_at

    def start(self):
        if self.is_running():
            raise Exception('Simulation is already running')

        random.seed(0)

        self._started_at = datetime.utcnow()

    def start_scenario(self, name: str, modifiers: Optional[dict] = None, options: Optional[dict] = None):
        if not self.is_running():
            raise Exception('Can not start scenario when simulation is not running')

        if self.scenario_is_running():
            self.running_scenario().end()

        self._scenarios.append(RunningScenario(
            name=name,
            started_at=datetime.utcnow(),
            modifiers=modifiers or {},
            options=options
        ))

    def current_modifiers(self):
        if not self.scenario_is_running():
            return {}

        return self.running_scenario().modifiers()

    def stop_running_scenario(self) -> RunningScenario:
        assert self.scenario_is_running(), "No scenario is running"

        scenario = self.running_scenario()

        scenario.end()

        return scenario

    def stop(self):
        if not self.is_running():
            raise Exception('Simulation is not running')

        if self.scenario_is_running():
            self.running_scenario().end()

        self._stopped_at = datetime.utcnow()

    def _finalise_last_scenario(self):
        pass

    def scenario_is_running(self):
        return len(self.running_scenarios()) > 0 and self.running_scenarios()[-1].is_running()

    def is_running(self) -> bool:
        return self._started_at is not None

    def running_scenario(self) -> Optional[RunningScenario]:
        if len(self.running_scenarios()) == 0:
            return None

        return self.running_scenarios()[-1]

    def running_scenarios(self) -> List[RunningScenario]:
        return self._scenarios


simulation: Simulation = Simulation()
