"""
Utilities for with-statement contexts
"""
import contextlib

# pylint: disable=invalid-name
#
import sys


class clictx(contextlib.AbstractContextManager):
    def __exit__(self, exctype, excinst, _exctb):
        if exctype is None:
            return True

        if issubclass(exctype, KeyboardInterrupt):
            # exit code could be success or error, it all depends on if it's the
            # normal way of quitting the app, so eat the exception by default.
            return True

        if issubclass(exctype, SystemExit):
            # sys.exit was called with an exit-code, then re-raise with value
            if isinstance(excinst, int):
                raise SystemExit(excinst)
            # sys.exit was called with an message, print and re-reaise with error
            print(excinst, file=sys.stderr)
            sys.exit(1)

        print(f"error: {excinst}", file=sys.stderr)
        sys.exit(1)
        return True


class suppress(contextlib.suppress, contextlib.ContextDecorator):
    """
    A version of contextlib.suppress with decorator support.

    Example
    -------

    .. code-block::

        @contextlib.suppress(ValueError)
        def foobar():
            ...
    """


class reraise_from_none(contextlib.suppress, contextlib.ContextDecorator):
    """
    Similar to contextlib.suppress, but with decorator support, and that
    re-raises exception from None instead of hiding it.

    Example
    -------

    .. code-block::

        @contextlib.reraise_from_none(ValueError)
        def foobar():
            ...
    """

    def __exit__(self, exctype, excinst, _exctb):
        if exctype is None:
            return
        if issubclass(exctype, self._exceptions):
            raise excinst from None
