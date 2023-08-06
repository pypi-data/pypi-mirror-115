import importlib
import pkgutil

from pynecone import ProtoCmd

from flask import Flask
app = Flask('pynecone')

class Server(ProtoCmd):

    def __init__(self):
        super().__init__('server',
                         'start server')

    def add_arguments(self, parser):
        pass #parser.add_argument('name', help="specifies the name of the component to be retrieved")

    def run(self, args):
        print('starting server')
        module = importlib.import_module('handlers')
        for pkg in [pkg_name for _, pkg_name, _ in pkgutil.iter_modules(['./handlers'])]:
            print('*** loading package {0}'.format(pkg))
            handler = getattr(module, pkg.title())()
            app.register_blueprint(handler.get_blueprint(), url_prefix='/' + handler.get_route_name())
        app.run()
