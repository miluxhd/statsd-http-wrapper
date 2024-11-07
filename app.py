from flask import Flask, request, jsonify
from statsd import StatsClient
import os
import time
import re
import json

app = Flask(__name__)

STATSD_HOST = os.getenv('STATSD_HOST', 'localhost')
STATSD_PORT = int(os.getenv('STATSD_PORT', 8125))

with open('metrics_whitelist.json', 'r') as f:
    metrics_config = json.load(f)

VALID_METRIC_NAME = re.compile(r"^[a-zA-Z_][a-zA9_]*$")

retries = 5
while retries > 0:
    try:
        statsd_client = StatsClient(host=STATSD_HOST, port=STATSD_PORT)
        break
    except Exception as e:
        retries -= 1
        print(f"StatsD connection failed: {e}. Retrying in 5 seconds...")
        time.sleep(5)
else:
    raise Exception("Could not connect to StatsD server after multiple attempts.")

@app.route('/counter', methods=['POST'])
def increment_counter():
    metric_name = request.args.get('metric')
    count = int(request.args.get('count', 1))  

    if not metric_name or metric_name not in metrics_config['metrics']:
        return "Invalid metric name. It must be whitelisted.", 400

    if not VALID_METRIC_NAME.match(metric_name):
        return "Invalid metric name format. Must start with a letter or underscore and contain only alphanumeric characters or underscores.", 400

    labels = {k: v for k, v in request.args.items() if k not in ['metric', 'count']}

    allowed_labels = metrics_config['metrics'][metric_name].get('labels', [])
    invalid_labels = [label for label in labels.keys() if label not in allowed_labels]
    if invalid_labels:
        return f"Invalid labels for {metric_name}: {', '.join(invalid_labels)}", 400

    metric_base = metric_name

    label_str = ','.join([f"{k}={v}" for k, v in labels.items()])

    if label_str:
        statsd_client.incr(f"{metric_base},{label_str}", count)
    else:
        statsd_client.incr(metric_base, count)

    return f"Incremented {metric_name} by {count} with labels {label_str if label_str else 'none'}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

