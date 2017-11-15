import graphene

from storage.core.sales.database import SalesDatabase


class DateAccumulated(graphene.ObjectType):
    year = graphene.Int()
    month = graphene.Int()
    day = graphene.Int()
    covers = graphene.Int()
    revenue = graphene.Float()


def result_to_dateaccumulated(result):
    return DateAccumulated(year=result["_id"].get("year"),
                           month=result["_id"].get("month"),
                           day=result["_id"].get("day"),
                           covers=result.get("covers"),
                           revenue=result.get("revenue"))


def results_to_dateaccumulated_array(results):
    date_accumulated = []
    for result in results:
        day_accumulated = result_to_dateaccumulated(result)
        date_accumulated.append(day_accumulated)
    return date_accumulated


arguments = {
    "venue_id": graphene.String(),
    "limit": graphene.Int(),
    "start_date": graphene.String(),
    "end_date": graphene.String(),
}


class Query(object):
    cover_by_day = graphene.List(DateAccumulated, **arguments)
    cover_by_week = graphene.List(DateAccumulated, **arguments)
    revenue_by_day = graphene.List(DateAccumulated, **arguments)
    revenue_by_week = graphene.List(DateAccumulated, **arguments)
    revenue_by_month = graphene.List(DateAccumulated, **arguments)
    snapshot_daily = graphene.List(DateAccumulated, **arguments)
    snapshot_monthly = graphene.List(DateAccumulated, **arguments)

    def resolve_cover_by_day(self, args, venue_id):
        days = SalesDatabase(venue_id).get_cover_by_day()
        return results_to_dateaccumulated_array(days)

    def resolve_cover_by_week(self, args, venue_id):
        weeks = SalesDatabase(venue_id).get_cover_by_week()
        return results_to_dateaccumulated_array(weeks)

    def resolve_revenue_by_day(self, args, venue_id):
        days = SalesDatabase(venue_id).get_revenue_by_day()
        return results_to_dateaccumulated_array(days)

    def resolve_revenue_by_week(self, args, venue_id):
        weeks = SalesDatabase(venue_id).get_revenue_by_week()
        return results_to_dateaccumulated_array(weeks)

    def resolve_revenue_by_month(self, args, venue_id):
        months = SalesDatabase(venue_id).get_revenue_by_month()
        return results_to_dateaccumulated_array(months)

    def resolve_snapshot_daily(self, args, venue_id, start_date=None, end_date=None, limit=None):
        snapshot = SalesDatabase(venue_id).get_snapshot_by_day()
        return results_to_dateaccumulated_array(snapshot)

    def resolve_snapshot_monthly(self, args, venue_id, start_date=None, end_date=None, limit=None):
        snapshot = SalesDatabase(venue_id).get_snapshot_by_month()
        return results_to_dateaccumulated_array(snapshot)
