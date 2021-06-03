from asyncio import wait


class EventHookAsync(object):
    """Class to implement an asynchronous event pattern

    Usage:  my_event_hook += my_func
            my_event_hook.invoke_async(args)

    """

    __handlers: list

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    async def invoke_async(self, *args, **keywargs):
        await wait([handler(*args, **keywargs) for handler in self.__handlers])
