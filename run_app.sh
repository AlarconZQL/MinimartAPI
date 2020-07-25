#!/bin/bash
export APP_SETTINGS_MODULE="config.development"
export FLASK_APP="entrypoint.py"
export FLASK_ENV="development"
flask run