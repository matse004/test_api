import graphene

# from schemas import venues, checks, reservations, vanity, labor, reports, check_items
from agnoris_api.schemas import checks


# class Query(venues.Query, checks.Query, reservations.Query, vanity.Query, labor.Query, reports.Query, check_items.Query,
#             graphene.ObjectType):
#     pass

class Query(checks.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
