class AutoReloader:
    def __init__(self, path):
        try:
            import os
            import uwsgi
            signal = [signum for signum in range(0,256) if not uwsgi.signal_registered(signum)][0]
            uwsgi.register_signal(signal, '', uwsgi.reload)
            for path in [x[0] for x in os.walk(path)]:
                uwsgi.add_file_monitor(signal, path.decode(encoding='UTF-8'))
        except Exception as err:
            pass # Not running under uwsgi. The other supported alternative is gunicorn. 
                 # Since gunicorn can be run with --max-requests=1 and doesn't require active reloading, do nothing
