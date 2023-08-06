# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Iterable, TypeVar

T = TypeVar("T")


class IAsyncEventHook(object):
    """
    event hook interface
    """

    async def trigger(self, message: T):
        raise NotImplementedError()


class IAsyncEventHooks(object):
    """
    event hooks interface
    """

    def register(self, hook_or_afunc: T) -> int:
        """
        注册
        :param hook_or_afunc:
        :return:
        """
        raise NotImplementedError()

    def unregister(self, hook_or_afunc: T) -> int:
        """
        移除
        :param hook_or_afunc:
        :return:
        """
        raise NotImplementedError()

    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError()


