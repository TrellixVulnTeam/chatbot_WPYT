#!/bin/sh
python3 -m rasa_nlu.server -c ./nlu_model_config.json
##启动 rasa_nlu，测试使用
##示例 curl -XPOST localhost:5000/parse -d '{"q":"查日志", "project": "bocbot", "model": "nlu_bocbot"}' | python -mjson.tool
