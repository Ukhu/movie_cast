export ENV='test'

export DATABASE_URL_TEST=''

flask db downgrade

flask db upgrade

python app.tests.py