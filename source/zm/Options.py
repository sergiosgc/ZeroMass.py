class Options:
    @staticmethod
    def get(name):
        try:
            import uwsgi
            return uwsgi.opt([name])
        except Exception as err:
            # We're not running wsgi. The other alternative is gunicorn, and an environment variable should be set with the config option
            import os
            return os.environ[name]
