"""
    Fastberry Main (Core-Methods)
"""
from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission

import spoc

# FrameWork
from .components import APIRouter as Router
from .components import cli
from .components import graphql as gql
from .framework import Fastberry as App

# GraphQL Tools
from .graphql import edges, error, errors, mutation, page, query

# GraphQL Premade User-Inputs
from .tools import Item as item
from .tools import Pagination as pagination


# Framework Wrappers
base_dir = spoc.base_dir
config = spoc.config
mode = spoc.mode
project = spoc.project
settings = spoc.settings

# Tools
component = spoc.component

try:
    import dbcontroller as dbc
    from dbcontroller.forms import ISNULL

    if hasattr(settings, "SQL_URL"):
        if settings.SQL_URL is not None:
            sql = dbc.Controller(sql=settings.SQL_URL)
    if hasattr(settings, "MONGO_URL"):
        if settings.MONGO_URL is not None:
            mongo = dbc.Controller(mongo=settings.MONGO_URL)

    # Types
    type = dbc.type

    # Forms
    input = dbc.form.graphql
    value = dbc.form.field

    # Value Tool
    filters = dbc.form.filters

    # Types Tool (DBController)
    field = dbc.field
    manager = dbc.manager

    # Scalars
    ID = dbc.ID
    date = dbc.date
    datetime = dbc.datetime
    time = dbc.time
    decimal = dbc.decimal
    text = dbc.text
    time = dbc.time
    json = dbc.json

    # Tester
    Date = dbc.Date

except ImportError:
    import strawberry

    # Types
    type = strawberry.type
    input = strawberry.input
