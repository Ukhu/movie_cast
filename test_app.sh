export ENV='test'

export TEST_DATABASE_URL=''

flask db downgrade

flask db upgrade

python app.tests.py