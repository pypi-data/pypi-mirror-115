# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import ReaderFactory, Encoding, PathTypes

from .base import IConfig
from .generator import ConfigGenerator
from .reader import ConfigReader


class IConfigFactory(object):

    @classmethod
    def create(cls, file: PathTypes, node: str) -> IConfig:
        raise NotImplementedError()


class ConfigFactory(IConfigFactory):

    @classmethod
    def create(cls, file: PathTypes, node: str) -> IConfig:
        reader = ReaderFactory.create(file, encoding=Encoding.UTF_8)
        config_reader = ConfigReader(reader, node)
        generator = ConfigGenerator(config_reader)
        return generator.generate()
