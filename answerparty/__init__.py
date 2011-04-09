from pyramid.config import Configurator
from answerparty.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('answerparty.views.my_view',
                    context='answerparty:resources.Root',
                    renderer='answerparty:templates/mytemplate.pt')
    config.add_static_view('static', 'answerparty:static')
    return config.make_wsgi_app()

