import graphene

from storage.core.sales.database import SalesDatabase
# from tivan.analysis.rds import VenueReportingDb
from storage.core.RDS.rds import VenueReportingDb



class DateAccumulated(graphene.ObjectType):
    year = graphene.Int()
    month = graphene.Int()
    day = graphene.Int()
    covers = graphene.Int()
    revenue = graphene.Float()
    this_week_revenue = graphene.Float()




def result_to_dateaccumulated(result):
    return DateAccumulated(year=result["_id"].get("year"),
                           month=result["_id"].get("month"),
                           day=result["_id"].get("day"),
                           covers=result.get("covers"),
                           revenue=result.get("revenue"),
                           this_week_revenue=result.get("this_week_revenue"),)

def rds_result_to_dateaccumulated(result):
    return DateAccumulated(year=result.get("year"),
                           month=result.get("month"),
                           day=result.get("day"),
                           covers=0,
                           revenue=0.0,
                           this_week_revenue=result.get("this_week_revenue"))

class PrevDateValues(graphene.ObjectType):
    _date = graphene.String()
    _value = graphene.Float()


class SnapshotCardRevenue(graphene.ObjectType):
    date = graphene.String()
    # prev_days_sales = graphene.String()
    # same_days_sales = graphene.String()
    prev_days_sales = graphene.List(PrevDateValues)
    same_days_sales = graphene.List(PrevDateValues)
    month_to_date_sales = graphene.Float()
    week_to_date_sales = graphene.Float()

def rds_result_to_revenue_card(result):

    last_days = []
    for day in result.get("prev_days_sales"):
        last_days.append(PrevDateValues(
            _date=day.get("_date")
            , _value=day.get("_value")
        ))

    last_same_days = []
    for day in result.get("prev_same_day_sales"):
        last_same_days.append(PrevDateValues(
            _date=day.get("_date")
            , _value=day.get("_value")
        ))

    card = SnapshotCardRevenue(
        date = result.get("ref_date")
        # , prev_days_sales = result.get("prev_days_sales")
        # , same_days_sales = result.get("prev_same_day_sales")
        , prev_days_sales=last_days
        , same_days_sales=last_same_days
        , month_to_date_sales = result.get("month_to_date_sales")
        , week_to_date_sales = result.get("week_to_date_sales")
    )

    return card

def rds_results_to_card_array(results):
    cards = []
    for result in results:
        card = rds_result_to_revenue_card(result)
        cards.append(card)
    return cards


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
    "ref_date": graphene.String()
}


class Query(object):
    cover_by_day = graphene.List(DateAccumulated, **arguments)
    cover_by_week = graphene.List(DateAccumulated, **arguments)
    revenue_by_day = graphene.List(DateAccumulated, **arguments)
    revenue_by_week = graphene.List(DateAccumulated, **arguments)
    revenue_by_month = graphene.List(DateAccumulated, **arguments)
    snapshot_daily = graphene.List(DateAccumulated, **arguments)
    snapshot_monthly = graphene.List(DateAccumulated, **arguments)
    revenue_this_week = graphene.List(DateAccumulated, **arguments)

    cards_revenue = graphene.List(SnapshotCardRevenue, **arguments)

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
        snapshot = SalesDatabase(venue_id).get_snapshot_by_day(limit=limit)
        return results_to_dateaccumulated_array(snapshot)

    def resolve_snapshot_monthly(self, args, venue_id, start_date=None, end_date=None, limit=None):
        snapshot = SalesDatabase(venue_id).get_snapshot_by_month(limit=limit)
        return results_to_dateaccumulated_array(snapshot)

    def resolve_revenue_this_week(self, args, ref_date, venue_id):
        revenue = VenueReportingDb(venue_id).checks_this_week_sales(ref_date)
        return [rds_result_to_dateaccumulated(revenue)]

    def resolve_cards_revenue(self, args, start_date, end_date, venue_id):
        cards = VenueReportingDb(venue_id).get_revenue_cards(start_date, end_date)
        return rds_results_to_card_array(cards)
