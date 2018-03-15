import graphene

from agnoris_api.schemas import checks, reservations, vanity, labor, check_items, reports, daily_report_rds


class Query(checks.Query, reservations.Query, vanity.Query, labor.Query, check_items.Query, reports.Query,
            daily_report_rds.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
