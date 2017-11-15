import graphene

from storage.core.labor.database import LaborDatabase


class WeekAccumulated(graphene.ObjectType):
    week = graphene.Int()
    position = graphene.String()
    shifts = graphene.Int()
    cost = graphene.Float()


def result_to_dateaccumulated(result):
    return WeekAccumulated(week=result["_id"].get("week"),
                           position=result["_id"].get("position"),
                           shifts=result.get("shifts"),
                           cost=result.get("cost"))


def results_to_dateaccumulated_array(results):
    weeks_accumulated = []
    for result in results:
        week_accumulated = result_to_dateaccumulated(result)
        weeks_accumulated.append(week_accumulated)
    return weeks_accumulated


arguments = {
    "venue_id": graphene.String(),
}


class Query(object):
    boh_shifts = graphene.List(WeekAccumulated, **arguments)
    foh_shifts = graphene.List(WeekAccumulated, **arguments)
    all_shifts = graphene.List(WeekAccumulated, **arguments)

    def resolve_boh_shifts(self, args, venue_id):
        shifts = LaborDatabase(venue_id).get_shift_report_boh()
        return results_to_dateaccumulated_array(shifts)

    def resolve_foh_shifts(self, args, venue_id):
        shifts = LaborDatabase(venue_id).get_shift_report_foh()
        return results_to_dateaccumulated_array(shifts)

    def resolve_all_shifts(self, args, venue_id):
        shifts = LaborDatabase(venue_id).get_shift_report()
        return results_to_dateaccumulated_array(shifts)
