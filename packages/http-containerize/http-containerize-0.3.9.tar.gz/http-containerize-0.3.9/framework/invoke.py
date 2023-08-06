from functools import reduce
import inspect
import os
import typing
import traceback

import flask
import cloudevents.http
from .locate import FindFunc, ArgumentConversion



def WrapFunction(func: typing.Callable) -> typing.Callable:
    sig = inspect.signature(func)
    args = [ArgumentConversion(p) for p in sig.parameters.values()]
    need_cloudevent = reduce(lambda a, b: a or b, (p.need_event for p in args))

    def handler() -> flask.Response:
        req = flask.request
        event = None
        if need_cloudevent:
            event = cloudevents.http.from_http(req.headers, req.get_data())
        
        params = {arg.name: arg.convert(req, event) for arg in args}

        result = func(**params)

        if isinstance(result, flask.Response):
            return result

        if need_cloudevent and result:
            try:
                headers, body = cloudevents.http.to_binary(result)
                return flask.Response(body, 200, headers)
            except Exception as e:
                print(f"Unable to decode result: {e}")
                traceback.print_exc()
                result = "Accepted with no event response"

        return flask.Response(result, 200)

    print(f"$$ Converting {inspect.signature(func)} to {inspect.signature(handler)}")
    return handler


def main():
    func = FindFunc(".")
    http_func = WrapFunction(func)
    # TODO: add option for GET / handle multiple functions
    app = flask.Flask(func.__name__)
    app.add_url_rule("/",view_func=http_func, methods=['POST'])
    app.run(port=os.environ.get("PORT", 8080))

