# coding: utf-8
from collections import namedtuple
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_scenario_testing.backend.Simulation import simulation

blueprint = Blueprint('scenario-testing', __name__)

Measurement = namedtuple('Measurement', ['time', 'measurement'])


def success(data: dict = None):
    return jsonify({'status': 'success', 'data': data})


def get_cpu_usage_measurements(start: datetime, end: datetime):
    from flask_scenario_testing.backend.initialise_scenario_testing import cpu_percents_measurements

    return [
        {'time': measurement.time.isoformat(), 'measurement': measurement.value}
        for measurement in cpu_percents_measurements
        if start <= measurement.time <= end
    ]


@blueprint.route('/api/simulation/start', methods=('POST',))
def start_simulation():
    print('Starting simulation')

    simulation.start()

    return success()


@blueprint.route('/api/simulation/start-scenario', methods=('POST',))
def start_new_scenario():
    data = request.json

    print('Starting new scenario')

    simulation.start_scenario(data['id'], data['modifiers'], data['options'], data['meta'])

    return success()


@blueprint.route('/api/simulation/stop-running-scenario', methods=('POST',))
def stop_running_scenario():
    print('Stopping running scenario')
    from flask_scenario_testing.backend.initialise_scenario_testing import latency_measurements
    simulation.stop_running_scenario()

    scenario = simulation.running_scenario()

    start = scenario.started_at()
    end = scenario.ended_at()

    cpu_usage_measurements = get_cpu_usage_measurements(start, end)

    data = {
        'id': scenario.id(),
        'cpu_usage_measurements': cpu_usage_measurements,
        'meta': scenario.meta(),
        'started_at': start.isoformat(),
        'ended_at': end.isoformat(),
        'endpoints': []
    }
    for (endpoint_name, measurements) in latency_measurements.items():
        data['endpoints'].append(dict(
            name=endpoint_name,
            latency_measurements=[
                dict(measurement=m.value, time=m.time.isoformat()) for m in measurements if start <= m.time <= end
            ]
        ))

    return success(data)


@blueprint.route('/api/simulation/stop', methods=('POST',))
def stop_simulation():
    from flask_scenario_testing.backend.initialise_scenario_testing import latency_measurements

    simulation.stop()

    endpoints = []
    for (endpoint_name, measurements) in latency_measurements.items():
        endpoints.append(dict(
            active=len(measurements) > 0,
            latency_measurements=[dict(
                measurement=m.value,
                time=m.time.isoformat()
            ) for m in measurements],
            name=endpoint_name,
            request_count=len(measurements)
        ))

    cpu_usage_measurements = get_cpu_usage_measurements(simulation.started_at(), simulation.stopped_at())

    scenario_data = []

    for scenario in simulation.running_scenarios():
        scenario_data.append(dict(
            start=scenario.started_at().isoformat(),
            end=scenario.ended_at().isoformat(),
            modifiers=scenario.modifiers(),
            name=scenario.id(),
            options=scenario.options()
        ))

    return jsonify(dict(
        started_at=simulation.started_at().isoformat(),
        stopped_at=simulation.stopped_at().isoformat(),
        scenarios=scenario_data,
        endpoints=endpoints,
        cpu_usage_measurements=cpu_usage_measurements
    ))


@blueprint.route('/api/measure-travel-time', methods=('POST',))
def measure_travel_time():
    return jsonify(dict(
        current_time=datetime.utcnow().isoformat()
    ))
