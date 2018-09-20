#!/bin/sh
python3 -m rasa_nlu.server -c ./nlu_model_config.json
curl -XPOST localhost:5000/parse -d '{"q":"查日志", "project": "bocbot", "model": "nlu_bocbot"}' | python -mjson.tool
