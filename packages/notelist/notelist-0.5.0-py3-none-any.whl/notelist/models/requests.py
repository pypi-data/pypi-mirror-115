"""Module with the database request models."""

from notelist.db import db
from notelist.tools import generate_uuid, get_current_ts


class Request(db.Model):
    """Database Request model.

    This table stores information about requests to URL and methods that have
    limits.
    """

    __tablename__ = "requests"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    address = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    created_ts = db.Column(db.Integer, nullable=False, default=get_current_ts)
    last_modified_ts = db.Column(
        db.Integer, nullable=False, default=get_current_ts)

    # Constraint: There can be only 1 record of a given combination of address,
    # URL and method.
    __table_args__ = (
        db.UniqueConstraint(
            address, url, method, name="un_requests_address_url_method"),)

    @classmethod
    def get(cls, address: str, url: str, method: str) -> "Request":
        """Return a request given its address, URL and method.

        :param address: Request address.
        :param url: Request URL.
        :param method: Request method.
        :return: `Request` instance.
        """
        return cls.query.filter_by(
            address=address, url=url, method=method).first()

    def save(self):
        """Save the request."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the request."""
        db.session.delete(self)
        db.session.commit()
