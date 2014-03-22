ZeroMass.py
===========

ZeroMass is a Python 3 minimalistic web application layer on top of wsgi. It provides:
 - HTTP Request decoding
 - HTTP Response encoding
 - A Hook mechanism allowing for the remainder of the software stack to actually answer requests.

Rationale
---------
WSGI, as defined in [PEP 333](http://legacy.python.org/dev/peps/pep-0333/), while being a non-leaky interface for writing web applications in Python, is a bit too low level for direct usage by application developers. The API is too close to the network layer, failing to provide an object oriented interface for exposing both the request data and the response in true OO fashion. While the WSGI approach is perfectly explained in PEP 333 and, I believe, correct, the API requires a few steps up in the abstraction axis to be really usable.

WSGI server documentation, namely for uwsgi and gunicorn, refer to Django, the top web development framework for Python, when faced with the natural need for a more abstract/powerful interface. The problem is that Django goes too far, locking development into an opinionated framework.

Opinionated frameworks are good. You can't build a stack as complete as Django without clear choices, and Django makes mostly good choices. However, there is space for a leaner approach. ZeroMass is such an approach. 

You may replace Django with Zope in the text above. The logic still holds.

Objective
---------
In the spirit of WSGI, ZeroMass raises the abstraction bar just a bit, in the hope of avoiding abstraction leakage. The goal set is this:
 - Parse the request, taking care of:
   - Parsing the request URL
   - Separating headers and request body
   - Decoding all textual content into utf-8
 - Encoding the response, taking care of:
   - Encoding headers
   - Encoding the body, if it is textual (as defined by its mime-type)
 - Connecting the request to whoever (function or method) in the application stack can answer it and return a response

Hello World
-----------
First, you need to get a wsgi server up and running, and pointing to the app.py script. It's a regular wsgi app, with two extras:
 - You must pass an environment variable called `zm_home` with the path to the application home directory
 - You must pass an environment variable called `zm_appname` with the name of the module to import for starting your application

ZeroMass will, during application setup — before accepting any request — load all modules in `$zm_home/$app_name`. You should take advantage of this and create a python script that contains one function or one static method that can answer the request, and place the file into `$zm_home/$app_name`. For a hello world, it should contain something in the line of:
```python
from zm import HookAfter

@HookAfter('zm.ZM.executeRequest')
def helloWorld(hookName, response, hookSelf, request, **kwargs):
    response.resultCode = 200
    response.setHeader('Content-type', 'text/plain')
    response.body = "Hello World"
    return (hookName, response, hookSelf, request, kwargs)
```

Other than a slightly complex method signature, the code is not too verbose. 
