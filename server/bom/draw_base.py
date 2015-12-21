import json
import datetime
from abc import ABCMeta, abstractmethod
import logging

from django.utils.translation import ugettext_lazy as _
from six import string_types
import pytz
import six


logger = logging.getLogger("echaloasuerte")


class InvalidDraw(RuntimeError):
    def __init__(self, attributes, message=None):
        """Initializes an invalid draw exception,

        attributes can be a string for a single attribute or a list of them
        """
        super(InvalidDraw, self).__init__(message)
        if isinstance(attributes, six.string_types):
            self.attributes = [attributes]
        else:
            self.attributes = attributes

        if message:
            self.message = message
        elif len(self.attributes) == 1:
            self.message = _("Invalid {0}").format(attributes)
        else:
            self.message = _("Invalid attributes: {0}").format(attributes)

    def __repr__(self):
        return "<Invalid Draw. Attr: '{}' msg: {}>".format(self.attributes,
                                                           self.message)

    def serialize(self):
        return json.dumps({'attributes': self.attributes,
                           'message': six.text_type(self.message)})


def get_utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


class BaseDraw(object):
    """
    Stores the content of a draw of random items
    """
    __metaclass__ = ABCMeta
    TYPES = {
        'creation_time': datetime.datetime,
        'owner': string_types,
        'users': list,
        'title': string_types,
        'enable_chat': bool,
        'is_shared': bool,
        'last_updated_time': datetime.datetime,
        'description': string_types
    }

    def __init__(self, creation_time=None, owner=None, number_of_results=1,
                 results=None, _id=None, draw_type=None,
                 users=None, title=None, is_shared=False,
                 enable_chat=True, last_updated_time=None,
                 audit=None, description=None, **kwargs):
        if kwargs:
            logger.info("Unexpected extra args: {0}".format(kwargs))

        self.number_of_results = number_of_results
        """Number of results to generate"""

        self.results = results if results else []
        """List of results (list of list of items)"""

        self._id = _id
        """Unique identifier of the draw"""

        self.owner = owner
        """ID of the owner of the draw"""

        from server import draw_factory

        self.draw_type = draw_factory.get_draw_name(type(self).__name__)
        """Type of the draw"""

        self.creation_time = creation_time if creation_time is not None else datetime.datetime.utcnow().replace(
            tzinfo=pytz.utc)
        """Time the draw was created"""

        self.last_updated_time = last_updated_time if last_updated_time else self.creation_time
        """last time this draw was updated"""

        self.users = users if users else []
        """List of users with access to the draw"""

        self.title = title
        """Title of the concrete draw"""

        self.description = description
        """Description of the draw"""

        self.audit = audit if audit else []
        """List of changes in the draw main config, user add_audit to add items"""

        self.enable_chat = enable_chat
        """Whether or not to display the chat"""

        self.is_shared = is_shared is True
        """Whether other users can see the draw"""

        # TODO: backward compat
        if "shared_type" in kwargs and kwargs["shared_type"]:
            self.is_shared = True

        if draw_type and draw_type != self.draw_type:
            logger.warning("A draw was built with type {0} but type {1} was "
                           "passed as argument! Fix it!"
                           .format(draw_type, self.draw_type))
        if self.last_updated_time.tzinfo is None:
            self.last_updated_time.replace(tzinfo=pytz.utc)
        if self.creation_time.tzinfo is None:
            self.creation_time.replace(tzinfo=pytz.utc)

    @property
    def pk(self):
        return str(self._id)

    def check_read_access(self, user):
        """Checks for read access"""
        if self.owner:
            return self.owner == user.pk or self.is_shared
        else:
            return True

    def check_write_access(self, user):
        """Checks whether user can write"""
        if self.owner is None:
            return True
        return user.pk == self.owner

    def check_types(self):
        """Check the types based on the class_attribute TYPES"""
        for attr, value in self.__dict__.items():
            if value and attr in self.TYPES:
                if not isinstance(value, self.TYPES[attr]):
                    raise InvalidDraw(attr,
                                      "{}: is '{}', expected: '{}'".format(
                                          attr, type(value), self.TYPES[attr]
                                      ))

    def validate(self):
        """Validates the draw. Throws if not valid"""
        self.check_types()
        if self.number_of_results < 1:
            raise InvalidDraw('number_of_results')
        if not self.title or len(self.title) > 500:
            raise InvalidDraw('title')
        if self.description and len(self.description) > 50000:
            raise InvalidDraw('description')

    def is_feasible(self):  # TODO: remove me
        return self.number_of_results > 0

    def mark_updated(self):
        """updated the last_updated_time of the draw to now"""
        self.last_updated_time = get_utc_now()

    def add_audit(self, type_):
        """Adds an audit message for the modification of a draw
        The latest audit are at the beginning
        the type of audits are:
        DRAW_PARAMETERS: one or more of the basic parameters of the draw changed
        """
        self.audit.insert(0, {
            "type": type_,
            "datetime": get_utc_now()
        })
        self.mark_updated()

    def toss(self):
        """Generates a new result for the draw"""
        result = {"datetime": get_utc_now(), "items": self.generate_result()}
        self.results.append(result)
        logger.debug("Tossed draw: {0}".format(self))
        logger.info("Generated result: {0}".format(result))
        return result

    def timed_toss(self, publication_datetime):
        """Adds a result with a publication time"""
        result = {
            "datetime": get_utc_now(),
            "items": self.generate_result(),
            "publication_datetime": publication_datetime
        }
        self.results.append(result)
        logger.debug("Scheduled draw toss: {0} ({1})".format(
            self, publication_datetime))
        return result


    @abstractmethod
    def generate_result(self):
        """This should return a list of generated results"""
        pass

    def __str__(self):
        return str(self.__dict__)
