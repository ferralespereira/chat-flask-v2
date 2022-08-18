# chat-Flask-v2
This is a Chat Web Site made it in Flask

## To Deploy in Ubuntu with Gunicorn and Apache2 server:

* Clone the project:
`git clone https://github.com/ferralespereira/chat-flask-v2.git`

* Go to project folder and create a venv (virtual enviroment):
`python3 -m venv venv`

* Activate venv:
`source venv/bin/activate`

* Install flask and this others package into venv:
`pip3 install flask; pip3 install flask-socketio; pip3 install wtforms`

* Install Gunicorn and eventlet:
`pip3 install gunicorn==20.1.0 eventlet==0.30.2`

* Create a "wsgi.py" file into your folder root like this:
```
from chat import app

if __name__ == '__main__':
    app.run() 

```

* Run gunicorn (to try if everything is working good so far):
`gunicorn --worker-class eventlet -w 1 wsgi:app`

* Deactivate virtual enviroment:
`deactivate`

### ----------*Second Part of Deploiment*--------------


* Create a file named "gunicorn_config.py" like this in the root of your project folder:
```
bind = 'unix:chatflaskv2.sock'
backlog = 2048

workers = 1
worker_class = 'eventlet'
worker_connections = 1000
timeout = 300
keepalive = 2

spew = False

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

loglevel = 'info'
errorlog = '/var/log/error.log'
accesslog = '/var/log/access.log'

proc_name = None

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")


    ## get traceback info
    import threading, sys, traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
```

* Create systemd Unit File (to allow Ubuntu’s init system to automatically start Gunicorn and serve Flask application whenever the server or your computer restarts:
`sudo nano /etc/systemd/system/chatflaskv2.service`
* Write this inside:
```
[Unit]
Description=Gunicorn instance to serve chat-flask-v2
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/html/chat-flask-v2
Environment="PATH=/var/www/html/chat-flask-v2/venv/bin"
ExecStart=/var/www/html/chat-flask-v2/venv/bin/gunicorn --config gunicorn_config.py wsgi:app

[Install]
WantedBy=multi-user.target
```

* Start and Enable the new service:
`sudo systemctl start chatflaskv2.service; sudo systemctl enable chatflaskv2.service`

* Reload, Restart and Status ststemctl:
`sudo systemctl daemon-reload; sudo systemctl restart chatflaskv2.service; sudo systemctl status chatflaskv2.service`

* Create the Apache host configuration file to look like this:
`sudo nano /etc/apache2/sites-enabled/000-default.conf`
```
# chat-flask-v2
<VirtualHost 127.0.0.10:80>
        ServerAdmin root@ubuntu

        ErrorLog ${APACHE_LOG_DIR}/chatflaskv2-error.log
        CustomLog ${APACHE_LOG_DIR}/chatflaskv2-access.log combined

        <Location />
                ProxyPass unix:/var/www/html/chat-flask-v2/chatflaskv2.sock|http://127.0.0.11/
                ProxyPassReverse unix:/var/www/html/chat-flask-v2/chatflaskv2.sock|http://127.0.0.11/
        </Location>
</VirtualHost>
```

* Reload the Apache2 service:
`sudo systemctl reload apache2`
