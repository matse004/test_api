import graphene

from datetime import datetime, timedelta

from storage.core.sales.database import SalesDatabase


# {'_id': {'dayOfYear': 262, 'dayOfMonth': 19, 'month': 9, 'year': 2017, 'item': 'Smoked Eggplant Carpaccio', 'price': 19.0}, 'count': 29}

class ItemsPerDay(graphene.ObjectType):
    day = graphene.Int()
    month = graphene.Int()
    year = graphene.Int()
    name = graphene.String()
    price = graphene.Float()
    count = graphene.Int()


class ItemsAccumulated(graphene.ObjectType):
    name = graphene.String()
    count = graphene.Int()


def result_to_items_per_day(result):
    return ItemsPerDay(year=result["_id"].get("year"),
                       month=result["_id"].get("month"),
                       day=result["_id"].get("dayOfMonth"),
                       name=result["_id"].get("item"),
                       price=result["_id"].get("price"),
                       count=result.get("count"))


def result_to_items_per_day_array(results):
    items_per_day = []
    for result in results:
        item = result_to_items_per_day(result)
        items_per_day.append(item)
    return items_per_day


def result_to_items_accumulated(result):
    return ItemsAccumulated(name=result["_id"], count=result["count"])


def result_to_items_accumulated_array(results):
    items_accumulated = []
    for result in results:
        item_accumulated = result_to_items_accumulated(result)
        items_accumulated.append(item_accumulated)
    return items_accumulated


arguments = {
    "venue_id": graphene.String(),
    "start_date": graphene.String(),
}


class Query(object):
    items_accumulated = graphene.List(ItemsAccumulated, **arguments)
    items_per_day = graphene.List(ItemsPerDay, **arguments)

    def resolve_items_accumulated(self, args, venue_id, start_date):
        if start_date is not None:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        else:
            start_date = datetime.today() - timedelta(days=7)
        items = SalesDatabase().get_items_count(start_date)
        return result_to_items_accumulated_array(items)

    def resolve_items_per_day(self, args, venue_id, start_date):
        if start_date is not None:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        else:
            start_date = datetime.today() - timedelta(days=7)
        items = list(SalesDatabase().get_items_by_day(datetime.today() - timedelta(days=7)))
        return result_to_items_per_day_array(items)
