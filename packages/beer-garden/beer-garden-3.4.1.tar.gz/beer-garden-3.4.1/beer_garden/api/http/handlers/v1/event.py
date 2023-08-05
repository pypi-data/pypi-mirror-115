# -*- coding: utf-8 -*-
import logging

from brewtils.errors import RequestForbidden
from tornado.web import HTTPError
from tornado.websocket import WebSocketHandler

from beer_garden.api.http.authorization import (
    AuthMixin,
    Permissions,
    check_permission,
    query_token_auth,
)

logger = logging.getLogger(__name__)


class EventSocket(AuthMixin, WebSocketHandler):

    closing = False
    listeners = set()

    auth_providers = frozenset([query_token_auth])

    def check_origin(self, origin):
        return True

    def open(self):
        if EventSocket.closing:
            self.close(reason="Shutting down")
            return

        # We can't go though the 'normal' BaseHandler exception translation
        try:
            check_permission(self.current_user, [Permissions.READ])
        except (HTTPError, RequestForbidden) as ex:
            self.close(reason=str(ex))
            return

        EventSocket.listeners.add(self)

    def on_close(self):
        EventSocket.listeners.discard(self)

    def on_message(self, message):
        pass

    @classmethod
    def publish(cls, message):
        # Don't bother if nobody is listening
        if not len(cls.listeners):
            return

        for listener in cls.listeners:
            listener.write_message(message)

    @classmethod
    def shutdown(cls):
        logger.debug("Closing websocket connections")
        EventSocket.closing = True

        for listener in cls.listeners:
            listener.close(reason="Shutting down")
