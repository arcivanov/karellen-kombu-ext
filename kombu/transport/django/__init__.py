"""Kombu transport using the Django database as a message store."""
from __future__ import absolute_import

from Queue import Empty

from anyjson import serialize, deserialize

from django.conf import settings
from django.core import exceptions as errors

from .. import virtual

from .models import Queue

VERSION = (0, 9, 4)
__version__ = ".".join(map(str, VERSION))

POLLING_INTERVAL = getattr(settings, "DJKOMBU_POLLING_INTERVAL", 5.0)


class Channel(virtual.Channel):

    def _new_queue(self, queue, **kwargs):
        Queue.objects.get_or_create(name=queue)

    def _put(self, queue, message, **kwargs):
        Queue.objects.publish(queue, serialize(message))

    def basic_consume(self, queue, *args, **kwargs):
        qinfo = self.state.bindings[queue]
        exchange = qinfo[0]
        if self.typeof(exchange).type == "fanout":
            return
        super(Channel, self).basic_consume(queue, *args, **kwargs)

    def _get(self, queue):
        #self.refresh_connection()
        m = Queue.objects.fetch(queue)
        if m:
            return deserialize(m)
        raise Empty()

    def _size(self, queue):
        return Queue.objects.size(queue)

    def _purge(self, queue):
        return Queue.objects.purge(queue)

    def refresh_connection(self):
        from django import db
        db.close_connection()


class Transport(virtual.Transport):
    Channel = Channel

    default_port = 0
    polling_interval = POLLING_INTERVAL
    connection_errors = ()
    channel_errors = (errors.ObjectDoesNotExist,
                      errors.MultipleObjectsReturned)
