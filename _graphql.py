import os

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers


def graphql_setup(app: web.Application) -> web.Application:
    """
    Setup all GraphQL settings
    """
    path = os.path.dirname(os.path.abspath(__file__))

    sdl_routes = (
        'questions',
    )

    endpoints = (
        'questions',
    )

    resolvers = (
        'questions.resolvers',
    )

    print([f'{path}/{route}' for route in sdl_routes])
    GQL = register_graphql_handlers(
        app=app,
        engine_sdl=[f'{path}/{route}' for route in sdl_routes][0],
        engine_modules=[x for x in resolvers][0],
        executor_http_endpoint=[f'{path}/{endpoint}' for endpoint in endpoints][0],
        executor_http_methods=["POST"],
        graphiql_enabled=True
    )

    return GQL
