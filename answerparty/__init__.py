from pyramid.config import Configurator
from answerparty.resources import Root
from answerparty.requestWithDB import RequestWithDB

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    
    config.set_request_factory(RequestWithDB)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('answerparty:templates')
    
    config.add_view('answerparty.views.my_view',
                    context='answerparty:resources.Root',
                    renderer='answerparty:templates/home.jinja2')
    
    config.add_static_view('static', 'answerparty:static')
    return config.make_wsgi_app()

