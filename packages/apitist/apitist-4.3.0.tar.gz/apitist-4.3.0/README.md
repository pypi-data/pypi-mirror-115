[![Build Status](https://github.com/zeburek/python-apitist/workflows/Python%20package/badge.svg)](https://github.com/zeburek/python-apitist/actions) [![PyPI version](https://badge.fury.io/py/apitist.svg)](https://badge.fury.io/py/apitist) [![Downloads](https://pepy.tech/badge/apitist)](https://pepy.tech/project/apitist)

# apitist

Brand new way to test your API

## Main features:

- Adding hooks for requests library
- Default hooks for:
    - Logging
    - Structuring/Unstructuring data

## Installation

Run the following command in your command line::
```bash
pip install apitist
```

If you want to use predefined random types please install additional requirements:
```bash
pip install -e apitist[random]
```

## Session and client creation

Session can take `base_url` parameter which will be used to prepend before requesting path.

```python
from apitist.requests import session

session = session("https://httpbin.org/v1")
session.get("/get") # Here request will be made to `https://httpbin.org/v1/get`
```

You can safely pass `path` and `base_url` with leading/forwarding slash:
```python
from apitist.requests import session

session("https://httpbin.org/v1").get("/get")
session("https://httpbin.org/v1/").get("/get")
session("https://httpbin.org/v1/").get("get")
session("https://httpbin.org/v1").get("get")
```

In all examples above requests would be made to `https://httpbin.org/v1/get`.

### Request decorators

Apitist offers all default requests types as a class method decorator, but there are some
requirements for that:

- Class, where you use decorators, should contain session parameter, with `Session` object
- Function, which is decorated, must return `None` or `dict` with parameters, that will be passed
to `request` function of `Session` object, like: `headers`, `data`, `json` and so on.
- You can use format placeholders in decorators `url` parameter, but you should remember that
parameters from method will be passed to `format` method AS IS - args to args, kwargs to kwargs.
As a result this code won't work:
  ```python
  class ExampleClient:
      ...

      @delete("/users/{id}?method={method}")
      def delete_user(self, id, method): ...
  ```

Example client class:

```python
from apitist import session
from apitist.decorators import get, post, put, delete


class ExampleClient:
    session = session("http://example.com/v1")

    @get("/users")
    def get_user(self): ...

    @get("/users/{}")
    def get_user(self, id): ...

    @post("/users")
    def create_user(self, data):
        return {"json": data}

    @put("/users/{}")
    def update_user(self, id, data):
        return {"json": data}

    @delete("/users/{}?method={method}")
    def delete_user(self, id, method="hide"): ...

```

## Shared Session

Shared Session class can be used to share cookies between different sessions.

```python
from apitist import session, SharedSession


s1 = session("https://google.com")
s2 = session("https://yandex.ru")

ss = SharedSession(s1, s2)

s2.get("/?q=2113")

assert s1.cookies == s2.cookies

s1.get("/?q=124")

assert s1.cookies == s2.cookies
```

## Default hooks

  - RequestDebugLoggingHook - logs request content with level DEBUG
  - RequestInfoLoggingHook - logs request content with level INFO
  - PrepRequestDebugLoggingHook - logs prepared request content (e.g. you will see query parameters in URL) with level DEBUG
  - PrepRequestInfoLoggingHook - logs prepared request content with level INFO
  - ResponseDebugLoggingHook - logs response content with level DEBUG
  - ResponseInfoLoggingHook - logs response content with level INFO
  - RequestAttrsConverterHook - converts attrs class in `data` field into json
  - RequestDataclassConverterHook - converts dataclass class in `data` field into json
  - ResponseAttrsConverterHook - adds `structure(type)` function to `requests.Response` class, which will structure
  response according to attrs class given to it
  - ResponseDataclassConverterHook - adds `structure(type)` function to `requests.Response` class, which will structure
  response according to dataclass class given to it

### Example usage

```python
from apitist import PrepRequestInfoLoggingHook, ResponseInfoLoggingHook
from apitist import session


s = session()
PrepRequestInfoLoggingHook.formatter = "Best formatter {req.method} {req.url}"

s.add_prep_request_hook(PrepRequestInfoLoggingHook)
s.add_response_hook(ResponseInfoLoggingHook)

s.post("https://httpbin.org/post", params={"q": "test"})
```

## Custom Hooks

```python
from requests import Request, PreparedRequest, Response

from apitist import session, RequestHook, PreparedRequestHook, ResponseHook

s = session()

class ReqHook(RequestHook):

    def run(self, request: Request) -> Request:
        print(request.url)
        return request

class PrepReqHook(PreparedRequestHook):

    def run(self, request: PreparedRequest) -> PreparedRequest:
        print(request.url)
        return request


class RespHook(ResponseHook):

    def run(self, response: Response) -> Response:
        print(response.url)
        return response

s.add_request_hook(ReqHook)
s.add_prep_request_hook(PrepReqHook)
s.add_response_hook(RespHook)

s.get("https://ya.ru", params={"q": "test"})
```

## Working with constructor

```python
import attr
import typing

from apitist import (
  converter,
  RequestConverterHook,
  ResponseConverterHook,
  session,
)


class ExampleType:
    test = None

@attr.s
class ExampleStructure:
    test: ExampleType = attr.ib()

@attr.s
class TestResponse:
    args: typing.Dict = attr.ib()
    data: str = attr.ib()
    files: typing.Dict = attr.ib()
    form: typing.Dict = attr.ib()
    headers: typing.Dict = attr.ib()
    json: ExampleStructure = attr.ib()
    origin: str = attr.ib()
    url: str = attr.ib()

s = session()
s.add_hook(RequestConverterHook)
s.add_hook(ResponseConverterHook)

def structure_example_type(data, type_):
    example = ExampleType()
    example.test = data
    return example

def unstructure_example_type(data):
    return data.test

converter.register_hooks(
    ExampleType, structure_example_type, unstructure_example_type
)

t = ExampleType()
t.test = "test"

struc = ExampleStructure(t)

res = s.post("https://httpbin.org/post", data=struc).structure(TestResponse)
print(res.structured.json.test.test) # test
```

## Using random data generator

First of all create an instance of random class:

```python
from apitist import Randomer
rand = Randomer()
```

Now, you can add custom hooks for different types:

```python
rand.add_type(str, lambda: str(random.random()))
rand.add_type(float, lambda: random.random())
```

Or using `add_types`:

```python
types = {
    str: lambda: str(random.random()),
    float: lambda: random.random()
}
rand.add_types(types)
```

Now you can create random object for given type or any attrs class with
defined types:

```python
import attr
import dataclasses
import typing

rand.object(str) # '0.6147789314561384'
rand.object(float) # 0.4664297665239271

@attr.s
class Data:
    value1: str = attr.ib()
    value2: typing.List[str] = attr.ib()
    value3: typing.Tuple[float] = attr.ib()

@dataclasses.dataclass
class Dataclass:
    value1: str
    value2: typing.List[str]
    value3: typing.Tuple[float]

print(rand.object(Data))
# Data(
#   value1='0.491058956716827',
#   value2=['0.6568036485871975'],
#   value3=(0.8603579349502298,)
# )

# Also works for dataclasses
print(rand.object(Dataclass))
# Data(
#   value1='0.491058956716827',
#   value2=['0.6568036485871975'],
#   value3=(0.8603579349502298,)
# )
```

It is better to use it with [Faker](https://github.com/joke2k/faker).
Just define different subclasses for `str` and add different hooks for them.
By this you could create different data for different `str` fields.

Also, using with `RequestConverterHook` and `ResponseConverterHook`
you could easily create random json objects which would be send to server.

## Predefined random types

```python
from apitist import Randomer
from apitist.random import Username, FirstName, LastName, Date
from dataclasses import dataclass


@dataclass
class LoginModel:
    username: Username
    password: str


@dataclass
class BookingDates:
    checkin: Date
    checkout: Date


@dataclass
class BookingModel:
    firstname: FirstName
    lastname: LastName
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str


rand = Randomer()
rand.add_predefined(locale="es-ES")
rand.object(LoginModel)
# LoginModel(
#   username='wfeliu',
#   password='VjHoHtLSjdoxXhtitaXU'
# )
rand.object(BookingModel)
# BookingModel(
#   firstname='Pedro',
#   lastname='Luz',
#   totalprice=931,
#   depositpaid=True,
#   bookingdates=BookingDates(checkin='1972-08-29', checkout='1971-05-19'),
#   additionalneeds='EFggHSpnzRSJATKtUmOm'
# )
```
