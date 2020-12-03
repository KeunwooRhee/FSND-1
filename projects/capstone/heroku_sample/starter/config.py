import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Database connection string
#if not database_path:
database_name = "capstonetest"
database_path = "postgres://{}:{}@{}/{}".format('rhee','projectpassword','localhost:5432', database_name)
# SQLALCHEMY_DATABASE_URI = 'postgres://<your database username>@localhost:5432/movies'
# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

