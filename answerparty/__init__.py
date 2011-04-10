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
    
    config.add_view('answerparty.views.home',
                    context='answerparty:resources.Root',
                    renderer='answerparty:templates/home.jinja2')
    config.add_route('makeRoom','/makeRoom',view='answerparty.views.make_room',renderer='json')
    config.add_route('joinRoom','/join',view='answerparty.views.join_room',renderer='json')
    config.add_static_view('static', 'answerparty:static')
    return config.make_wsgi_app()

