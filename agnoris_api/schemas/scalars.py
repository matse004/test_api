import json
import datetime

from graphql.language import ast

from graphene.types.scalars import Scalar


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


class JSONObjectString(Scalar):
    '''JSON String'''

    @staticmethod
    def serialize(dt):
        return json.dumps(dt, default=datetime_handler)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return json.loads(node.value)

    @staticmethod
    def parse_value(value):
        return json.loads(value)
