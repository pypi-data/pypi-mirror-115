from enum import IntEnum

from django.http import JsonResponse


class Code(IntEnum):
    ERROR = 0
    SUCCESS = 1
    FAILED = 2


def error_dict(msg: str) -> dict:
    return {"code": Code.FAILED, "msg": msg, "data": {}}


def error_response(msg: str) -> JsonResponse:
    return JsonResponse(data=error_dict(msg))


def success_dict(msg: str, data: dict) -> dict:
    return {"code": Code.SUCCESS, "msg": msg, "data": data}


def success_response(msg: str, data: dict) -> JsonResponse:
    return JsonResponse(data=success_dict(msg, data))
