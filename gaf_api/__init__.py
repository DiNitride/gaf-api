from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # API v1
    config.add_route('v1:calendar/events', '/api/v1/calendar/events')

    config.scan()
    return config.make_wsgi_app()
