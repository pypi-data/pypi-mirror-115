import json

from django_helper import test
from ..code import Code, error_response, success_response


def test_code_enum_value():
    assert hasattr(Code, "SUCCESS")
    assert Code.SUCCESS == 1


def test_success_response():
    res = success_response(msg="hello", data="test")
    res = res.content
    res = json.loads(res)
    test.assert_code(res, Code.SUCCESS)


def test_error_response():
    res = error_response(msg="hello")
    res = res.content
    res = json.loads(res)
    test.assert_code(res, Code.FAILED)
