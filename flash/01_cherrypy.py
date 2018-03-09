import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "<h1>Hello world 2!</h2>"


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
