import inspect

from .. import contracts


async def _shutdown_instance(callback_function, instance: contracts.SingletonInstance):
    if not instance:
        return
    if inspect.iscoroutinefunction(callback_function):
        await callback_function(instance)
    elif callable(callback_function):
        callback_function(instance)
