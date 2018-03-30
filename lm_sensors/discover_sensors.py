#!/usr/bin/env python
from __future__ import print_function

import json
import re
import subprocess

result = subprocess.check_output(['sensors', '-A', '-u']).decode("utf-8")

sensors = {}

###
# Collect sensor data
###

# Helper variables
cur_adapter = None
cur_sensor = None

for line in result.split("\n"):
    if not line:
        # Empty lines most likely indicate a new adapter, thus reset all helper
        cur_adapter = None
        cur_sensor = None
        continue

    # The first line is always the adapter
    if not cur_adapter:
        cur_adapter = line
        sensors[cur_adapter] = {}
        continue

    # If sensor is null or line has no whitespace char we have a new sensor
    if not cur_sensor or re.match(r'\S', line):
        cur_sensor = line[:-1]
        sensors[cur_adapter][cur_sensor] = {}
        continue

    # Get sensor detail info
    line = line.split('_', 1)[-1]  # strip "  something_"
    parts = line.split(":")
    sensors[cur_adapter][cur_sensor][parts[0]] = parts[1].split(".")[0].strip()

complete = {"data": []}

# Reformat data
for adapter, adapter_values in sensors.items():
    for sensor, sensor_values in adapter_values.items():
        data = {"{#ADAPTER}": adapter, "{#SENSOR}": sensor}

        for item, value in sensor_values.items():
            data["{#" + item.upper() + "}"] = value

        complete["data"].append(data)

out = json.dumps(complete)
print(out)
