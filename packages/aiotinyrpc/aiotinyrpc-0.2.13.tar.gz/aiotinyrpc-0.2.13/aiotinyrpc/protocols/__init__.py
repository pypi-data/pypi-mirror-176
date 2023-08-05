#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Protocol definition.

Defines the abstract base classes from which a protocol definition must be constructed.
"""
from abc import ABC
from typing import Any, Generator, List, Dict, Union, Optional
import itertools

from aiotinyrpc import exc


class RPCRequest(object):
    """Defines a generic RPC request."""

    def __init__(self) -> None:
        self.unique_id = None
        """Correlation ID used to match request and response.

        :type: int or str or None

        Protocol specific, may or may not be set.
        This value should only be set by :py:func:`~tinyrpc.protocols.RPCProtocol.create_request`.

        When the protocol permits it this ID allows servers to respond to requests out
        of order and allows clients to relate a response to the corresponding request.

        Only supported if the protocol has its
        :py:attr:`~tinyrpc.protocols.RPCProtocol.supports_out_of_order` set to ``True``.

        Generated by the client, the server copies it from request to corresponding response.
        """

        self.method = None
        """The name of the RPC function to be called.

        :type: str

        The :py:attr:`method` attribute uses the name of the function as it is known by the public.
        The :py:class:`~tinyrpc.dispatch.RPCDispatcher` allows the use of public aliases in the
        ``@public`` decorators.
        These are the names used in the :py:attr:`method` attribute.
        """

        self.args = []
        """The positional arguments of the method call.

        :type: list

        The contents of this list are the positional parameters for the :py:attr:`method` called.
        It is eventually called as ``method(*args)``.
        """

        self.kwargs = {}
        """The keyword arguments of the method call.

        :type: dict

        The contents of this dict are the keyword parameters for the :py:attr:`method` called.
        It is eventually called as ``method(**kwargs)``.
        """

    def error_respond(
        self, error: Union[Exception, str]
    ) -> Optional["RPCErrorResponse"]:
        """Creates an error response.

        Create a response indicating that the request was parsed correctly,
        but an error has occurred trying to fulfill it.

        This is an abstract method that must be overridden in a derived class.

        :param error: An exception or a string describing the error.
        :type error: Exception or str
        :return: A response or ``None`` to indicate that no error should be sent out.
        :rtype: :py:class:`RPCErrorResponse`
        """
        raise NotImplementedError()

    def respond(self, result: Any) -> Optional["RPCResponse"]:
        """Create a response.

        Call this to return the result of a successful method invocation.

        This creates and returns an instance of a protocol-specific subclass of
        :py:class:`~tinyrpc.RPCResponse`.

        This is an abstract method that must be overridden in a derived class.

        :param result: Passed on to new response instance.
        :type result: Any type that can be serialized by the protocol.

        :return: A response or ``None`` to indicate this request does not expect a response.
        :rtype: :py:class:`RPCResponse`
        """
        raise NotImplementedError()

    def serialize(self) -> bytes:
        """Returns a serialization of the request.

        Converts the request into a bytes object that can be passed to and by the transport layer.

        This is an abstract method that must be overridden in a derived class.

        :return: A bytes object to be passed on to a transport.
        :rtype: bytes
        """
        raise NotImplementedError()


class RPCBatchRequest(list):
    """Multiple requests batched together.

    Protocols that support multiple requests in a single message use this to group them together.
    Note that not all protocols may support batch requests.

    Handling a batch requests is done in any order, responses must be gathered
    in a batch response and be in the same order as their respective requests.

    Any item of a batch request is either an :py:class:`RPCRequest` or an
    :py:class:`~tinyrpc.exc.BadRequestError`, which indicates that there has been
    an error in parsing the request.
    """

    def create_batch_response(self) -> Optional["RPCBatchResponse"]:
        """Creates a response suitable for responding to this request.

        This is an abstract method that must be overridden in a derived class.

        :return: An :py:class:`RPCBatchResponse` or None if no response is expected.
        :rtype: :py:class:`RPCBatchResponse`
        """
        raise NotImplementedError()

    def serialize(self) -> bytes:
        """Returns a serialization of the request.

        Converts the request into a bytes object that can be passed to and by the transport layer.

        This is an abstract method that must be overridden in a derived class.

        :return: A bytes object to be passed on to a transport.
        :rtype: bytes
        """
        raise NotImplementedError()


class RPCResponse(ABC):
    """Defines a generic RPC response.

    Base class for all responses.

    .. py:attribute:: id

        Correlation ID to match request and response

        :type: str or int

    .. py:attribute:: result

        When present this attribute contains the result of the RPC call.
        Otherwise the :py:attr:`error` attribute must be defined.

        :type: Any type that can be serialized by the protocol.

    .. py:attribute:: error

        When present the :py:attr:`result` attribute must be absent.
        Presence of this attribute indicates an error condition.

        :type: :py:class:`~tinyrpc.exc.RPCError`
    """

    def __init__(self) -> None:
        self.unique_id = None
        """Correlation ID used to match request and response.

        :type: int or str or None
        """

    def serialize(self) -> bytes:
        """Returns a serialization of the response.

        Converts the response into a bytes object that can be passed to and by the transport layer.

        This is an abstract method that must be overridden in a derived class.

        :return: The serialized encoded response object.
        :rtype: bytes
        """
        raise NotImplementedError()


class RPCErrorResponse(RPCResponse, ABC):
    """RPC error response class.

    Base class for all deriving responses.

    .. py:attribute:: error

        This attribute contains the fields ``message`` (str) and
        ``code`` (int) where at least ``message`` is required to contain a value.

        :type: dict
    """

    error = None


class RPCBatchResponse(list):
    """Multiple response from a batch request. See
    :py:class:`RPCBatchRequest` on how to handle.

    Items in a batch response need to be
    :py:class:`RPCResponse` instances or None, meaning no reply should
    generated for the request.
    """

    def serialize(self) -> bytes:
        """Returns a serialization of the batch response.

        Converts the response into a bytes object that can be passed to and by the transport layer.

        This is an abstract method that must be overridden in a derived class.

        :return: A bytes object to be passed on to a transport.
        :rtype: bytes
        """
        raise NotImplementedError()


class RPCProtocol(ABC):
    """Abstract base class for all protocol implementations."""

    supports_out_of_order = False
    """If true, this protocol can receive responses out of order correctly.

    Note that this usually depends on the generation of unique_ids, the
    generation of these may or may not be thread safe, depending on the
    protocol. Ideally, only one instance of RPCProtocol should be used per
    client.

    :type: bool
    """

    raises_errors = True
    """If True, this protocol instance will raise an RPCError exception.

    On receipt of an RPCErrorResponse instance an RPCError exception is raised.
    When this flag is False the RPCErrorResponse object is returned to the caller
    which is then responsible for handling the error.

    :type: bool
    """

    def create_request(
        self,
        method: str,
        args: List[Any] = None,
        kwargs: Dict[str, Any] = None,
        one_way: bool = False,
    ) -> "RPCRequest":
        """Creates a new :py:class:`RPCRequest` object.

        Called by the client when constructing a request.
        It is up to the implementing protocol whether or not ``args``,
        ``kwargs``, one of these, both at once or none of them are supported.

        :param str method: The method name to invoke.
        :param list args: The positional arguments to call the method with.
        :param dict kwargs: The keyword arguments to call the method with.
        :param bool one_way: The request is an update, i.e. it does not expect a reply.
        :return: A new request instance
        :rtype: :py:class:`RPCRequest`
        """
        raise NotImplementedError()

    def parse_request(self, data: bytes) -> "RPCRequest":
        """De-serializes and validates a request.

        Called by the server to reconstruct the serialized :py:class:`RPCRequest`.

        :param bytes data: The data stream received by the transport layer containing the
            serialized request.
        :return: A reconstructed request.
        :rtype: :py:class:`RPCRequest`
        """
        raise NotImplementedError()

    def parse_reply(self, data: bytes) -> Union["RPCResponse", "RPCBatchResponse"]:
        """De-serializes and validates a response.

        Called by the client to reconstruct the serialized :py:class:`RPCResponse`.

        :param bytes data: The data stream received by the transport layer containing the
            serialized response.
        :return: A reconstructed response.
        :rtype: :py:class:`RPCResponse`
        """
        raise NotImplementedError()

    def raise_error(self, error: "RPCErrorResponse") -> exc.RPCError:
        """Raises the exception in the client.

        Called by the client to convert the :py:class:`RPCErrorResponse` into an Exception
        and raise or return it depending on the :py:attr:`raises_errors` attribute.

        :param error: The error response received from the server.
        :type error: :py:class:`RPCResponse`
        :rtype: :py:exc:`~tinyrpc.exc.RPCError` when :py:attr:`raises_errors` is False.
        :raises: :py:exc:`~tinyrpc.exc.RPCError` when :py:attr:`raises_errors` is True.
        """
        ex = exc.RPCError("Error calling remote procedure: %s" % error.error["message"])
        if self.raises_errors:
            raise ex
        return ex


class RPCBatchProtocol(RPCProtocol, ABC):
    """Abstract base class for all batch protocol implementations."""

    def create_batch_request(
        self, requests: List["RPCRequest"] = None
    ) -> "RPCBatchRequest":
        """Create a new :py:class:`RPCBatchRequest` object.

        Called by the client when constructing a request.

        :param requests: A list of requests.
        :type requests: :py:class:`list` or :py:class:`RPCRequest`
        :return: A new request instance.
        :rtype: :py:class:`RPCBatchRequest`
        """
        raise NotImplementedError()


def default_id_generator(start: int = 1) -> Generator[int, None, None]:
    """Generates sequential integers from `start`.

    e.g. 1, 2, 3, .. 9, 10, 11, ...

    :param start: The first value to start with.`
    :type start: int
    :return: A generator that yields a sequence of integers.
    :rtype: :py:class:`Generator[int, None, None]`
    """
    return itertools.count(start)
