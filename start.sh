#!/bin/sh
python3 -m rasa_core.server -d ./models/dialogue -u ./models/bocbot/nlu_bocbot -o out.log
