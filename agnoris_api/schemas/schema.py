import graphene

# checks, reservations, vanity, labor, check_items, reports,
from agnoris_api.schemas import daily_report_rds

# checks.Query, reservations.Query, vanity.Query, labor.Query, check_items.Query, reports.Query,
class Query(daily_report_rds.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
