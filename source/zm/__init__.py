from zm.Hook import Hook,HookBefore,HookAfter
from zm.AutoReloader import AutoReloader
from zm.Options import Options
from zm.HTTPRequest import HTTPRequest
from zm.HTTPResponse import HTTPResponse

class ZM(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ZM, cls).__new__(cls, *args, **kwargs)
            cls._instance.autoLoadModules()

        return cls._instance

    def __init__(self):
        if 'runtimeInitialized' not in self.__dict__: # Don't reinitalize singleton
            self.preHooks = {}
            self.postHooks = {}
            self.runtimeInitialized = False

    def registerPreHook(self, hookName, function):
        if hookName not in self.preHooks:
            self.preHooks[hookName] = []
        self.preHooks[hookName].append(function)
    
    def registerPostHook(self, hookName, function):
        if hookName not in self.postHooks:
            self.postHooks[hookName] = []
        self.postHooks[hookName].append(function)

    def hookPre(self, hookName, packedArgs):
        print("Hookpre for %s" % hookName)
        (fn, args, kwargs) = packedArgs
        if hookName in self.preHooks:
            argsForHook = tuple([hookName, fn] + list(args))
            for hook in self.preHooks[hookName]:
                (argsForHook, kwargs) = hook(*argsForHook, **kwargs)
            fn = argsForHook[1]
            args = argsForHook[2:]
        return (fn, args, kwargs)

    def hookPost(self, hookName, packedArgs):
        print("Hookpost for %s" % hookName)
        (retVal, args, kwargs) = packedArgs
        if hookName in self.postHooks:
            argsForHook = tuple([hookName, retVal] + list(args))
            for hook in self.postHooks[hookName]:
                (argsForHook, kwargs) = hook(*argsForHook, **kwargs)
            retVal = argsForHook[1]
        return retVal

    def autoLoadModules(self, modulePath = None):
        import os.path
        if modulePath is None:
            self.home = Options.get('zm_home')
            modulesPath = os.path.join(self.home, Options.get('zm_appname'))
            return self.autoLoadModules(modulesPath)
        else:
            import pkgutil
            import sys
            if self.home != modulePath[0:len(self.home)]:
                raise Exception("Trying to import module path " + modulePath + " from subtree other than application home: " + self.home)
            for importer, package_name, _ in pkgutil.iter_modules([modulePath]):
                full_package_name = '%s.%s' % (modulePath[len(self.home)+1:], package_name)
                if full_package_name not in sys.modules:
                    __import__(full_package_name, locals(), globals())

    def answerRequest(self, env, start_response):
        try:
            if not self.runtimeInitialized:
                self.runtimeInit()

            url = env['wsgi.url_scheme'] + "//" + env['HTTP_HOST'] + env['RAW_URI']
            request = HTTPRequest(url, env['REQUEST_METHOD'], protocolVersion=env['SERVER_PROTOCOL'].split('/', 2)[1])
            for key,value in dict((key[len('HTTP_'):],value) for key,value in env.items() if key.startswith('HTTP_')).items():
                request.addHeader(key, value)
            for wsgiField in ['SERVER_PORT', 'REMOTE_ADDR', 'REMOTE_PORT', 'wsgi.multiprocess', 'PATH_INFO', 'wsgi.version', 'SERVER_NAME', 'SERVER_SOFTWARE', 'SERVER_PROTOCOL', 'SCRIPT_NAME', 'wsgi.run_once', 'wsgi.multithread']:
                if wsgiField in env:
                    if wsgiField.startswith('wsgi.'):
                        request.addHeader(wsgiField, env[wsgiField])
                    else:
                        request.addHeader("wsgi." + wsgiField, env[wsgiField])
            response = self.executeRequest(request)
            if response.resultCode == 0:
                raise Exception("Request execution did not result in a response with a status code")

            start_response('200 OK', [('Content-Type','text/html')])
            return [b"Hello World"]
        except Exception as e:
            import sys
            import traceback
            start_response('500 Python Exception', [('Content-Type','text/plain')])
            print(e)
            return [b"HTTP 500: Internal server error; Python exception caught by top level handler\n\n", bytes(str(e), 'utf-8'), b"\n\n", bytes(traceback.format_exc(), 'utf-8')]

    @Hook
    def runtimeInit(self):
        self.runtimeInitialized = True

    @Hook
    def executeRequest(self, request):
        result = HTTPResponse()
        return result

