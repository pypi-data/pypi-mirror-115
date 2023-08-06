"""Database module."""

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Database object
db = SQLAlchemy(metadata=MetaData())

# Serialization object
ma = Marshmallow()
