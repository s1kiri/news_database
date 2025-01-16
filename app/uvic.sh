#!/bin/bash

CONFIG_PATH="configs/config.yaml"

HOST=$(python -c "import yaml; config = yaml.safe_load(open('$CONFIG_PATH')); print(config['api']['host'])")
PORT=$(python -c "import yaml; config = yaml.safe_load(open('$CONFIG_PATH')); print(config['api']['port'])")
LOG_LEVEL=$(python -c "import yaml; config = yaml.safe_load(open('$CONFIG_PATH')); print(config['api']['log_level'])")
RELOAD=$(python -c "import yaml; config = yaml.safe_load(open('$CONFIG_PATH')); print(config['api']['reload'])")

uvicorn app:app --host $HOST --port $PORT --log-level $LOG_LEVEL --reload