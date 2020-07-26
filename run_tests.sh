#!/bin/bash
export APP_SETTINGS_MODULE="config.testing"
export FLASK_ENV="testing"
echo "RUNNING TESTS..."
coverage run -m unittest discover
echo "GENERATING COVERAGE REPORTS..."
coverage report -m app/*/*.py