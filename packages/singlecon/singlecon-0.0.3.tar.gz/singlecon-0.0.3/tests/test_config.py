import logging
import os
from pathlib import Path
import pytest
from pydantic import ValidationError, PrivateAttr, BaseModel

from singlecon import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# pytest tests/test_config.py --log-cli-level DEBUG 

@pytest.fixture
def env_path():
    conf_path = "tests/data/.env"
    p = Path(conf_path)
    p.unlink(missing_ok=True)
    yield conf_path
    # clean the path before and after use
    p.unlink(missing_ok=True)

@pytest.fixture
def persist_env_path():
    conf_path = "tests/data/.env"
    p = Path(conf_path)
    p.unlink(missing_ok=True)
    yield conf_path

@pytest.fixture
def conf_path():
    conf_path = "tests/data/config.toml"
    p = Path(conf_path)
    p.unlink(missing_ok=True)
    yield conf_path
    # clean the path before and after use
    p.unlink(missing_ok=True)

@pytest.fixture
def persist_conf_path():
    conf_path = "tests/data/config.toml"
    p = Path(conf_path)
    p.unlink(missing_ok=True)
    yield conf_path

def test_env_dict(monkeypatch, env_path):
    class SubConfig(TemplateConfig):
        a = 4
        b = 5
    SubConfig._env_fields = ['a']
    sub_config = SubConfig(a=7)
    class MockConfig(TemplateConfig):
        a = 1
        b = 2
        c = 3
        sub_c = sub_config
        class Config:
            env_nested_delimiter = '_'
    MockConfig._env_fields = ['a','b']
    config = MockConfig(a=0)

    env_d = config.env_dict()
    
    assert config.env_dict() == {'A': 0, 'B': 2, 'SUB_C_A': 7}

    with pytest.raises(ValidationError) as excinfo:
        monkeypatch.setenv('SUB_C_A', '10')
        config = MockConfig()
    assert "value_error.extra" in str(excinfo.value)
    assert os.getenv('SUB_C_A') == '10'

    config.__config__.env_nested_delimiter = '__'
    config.to_dotenv(env_file=env_path)

    class ReadEnv(MockConfig):
        class Config:
            env_file = env_path

    read_conf = ReadEnv()
    assert read_conf.a == 0
    assert read_conf.sub_c.a == 7
    assert read_conf.dict() == config.dict()

    logger.debug({k:v for k,v in config})
    logger.debug(config.dict())
    logger.debug(type(MockConfig))

def test_multiple_inherit():
    class A(TemplateConfig):
        a = 1
    
    class B(TemplateConfig):
        a = 2
        b = 3

    class C(A, B, EnvConfig):
        a = 4
        c = 5
        d: str

    logger.debug(C.__fields__)
    logger.debug({k:v for k,v in C(c=2,d=45)})
    logger.debug(C(d=45).dict())
    assert C._env_fields == ['d', 'c']
    with pytest.raises(ValidationError, match='field required'):
        assert C().a == 4

    class D(A, B, EnvConfig):
        a = 4
        c: str = 5
        d: str

    assert D._env_fields == ['c', 'd']

def test_file_config(monkeypatch, conf_path, env_path):
    class SubConfig(TemplateConfig):
        a = 4
        b = 5
    SubConfig._env_fields = ['a']
    sub_config = SubConfig(a=7)
    class MockConfig(FileConfig):
        a = 1
        b = 2
        c = 3
        sub_c = sub_config

    assert not MockConfig._extra_env
    
    class EnvMock(extra_env(MockConfig)):
        env_field: str

    assert not MockConfig._extra_env
    assert not EnvMock._extra_env
    MockConfig(a=0)
    logger.debug(MockConfig._file_fields)
    assert MockConfig._file_fields == ['a', 'b', 'c', 'sub_c']
    logger.debug(MockConfig._env_fields)
    assert MockConfig._env_fields == []
    logger.debug(EnvMock._env_fields)
    assert EnvMock._env_fields == ['env_field']

    class MorePyConfig(EnvMock):
        a = -1
        pythonic = {
            'a': 1,
            'b': 2,
        }
    assert MorePyConfig._file_fields == ['a', 'b', 'c', 'sub_c']
    assert MorePyConfig._env_fields == ['env_field']

    pyc = MorePyConfig(env_field='abc')
    pyc.sub_c.a = -10
    pyc.to_dotenv(env_file=env_path)

    with pytest.raises(ValidationError, match='env_field'):    
        MorePyConfig()

    pyconfig = MorePyConfig(_env_file=env_path)
    assert pyconfig.sub_c.a == -10
    logger.debug(pyconfig.dict())
    assert pyconfig.dict() == {'a': -1, 'b': 2, 'c': 3, 'sub_c': {'a': -10, 'b': 5}, 'env_field': 'abc', 'pythonic': {'a': 1, 'b': 2}}

    with pytest.raises(ValidationError, match='env_field'):    
        config = EnvMock(a=0)

    assert not MockConfig._extra_env
    class MoreEnv(MockConfig, EnvConfig):
        env_var = 99

    assert not MockConfig._extra_env
    assert MoreEnv._env_fields == ['env_var']
    assert not MoreEnv._extra_env
    logger.debug(MoreEnv().dict())

    class MoreEnv(MockConfig):
        env_var = 99

