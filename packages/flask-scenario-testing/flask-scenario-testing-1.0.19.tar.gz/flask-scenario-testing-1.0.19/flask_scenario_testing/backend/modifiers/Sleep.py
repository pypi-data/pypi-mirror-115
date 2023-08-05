from flask_scenario_testing.backend.modifiers.Modifier import Modifier
from time import sleep


class Sleep(Modifier):
    def identifier(self):
        return 'SLEEP'

    def modify(self, fun, endpoint_name, modifier_args: dict):
        def wrapper(*args, **kwargs):
            sleep_ms = int(modifier_args.get('time'))
            sleep_for = sleep_ms / 1000
            print('Sleeping for {}ms'.format(sleep_ms))
            sleep(sleep_for)

            return fun(*args, **kwargs)

        return wrapper
