import graphene

from storage.core.venue.database import VenueDatabase


class PaymentMethod(graphene.ObjectType):
    type = graphene.String()
    provider = graphene.String()
    provider_id = graphene.String()


class Payment(graphene.ObjectType):
    payment_method = graphene.Field(PaymentMethod)
    tip = graphene.Float()
    amount = graphene.Float()


class Server(graphene.ObjectType):
    name = graphene.String()
    provider_id = graphene.String()


class Table(graphene.ObjectType):
    name = graphene.String()
    number = graphene.String()
    covers = graphene.Int()


class CheckItem(graphene.ObjectType):
    name = graphene.String()
    price = graphene.Float()


class Check(graphene.ObjectType):
    db_id = graphene.String()
    provider_id = graphene.String()
    covers = graphene.Int()
    date = graphene.String()
    server = graphene.Field(Server)
    check_number = graphene.String()
    table_number = graphene.Field(Table)
    total_paid_amount = graphene.Float()
    subtotal = graphene.Float()
    tax = graphene.Float()
    tip = graphene.Float()
    items = graphene.List(CheckItem)
    payments = graphene.List(Payment)


arguments = {
    "venue_id": graphene.String(),
    "limit": graphene.Int(),
    "start_date": graphene.String(),
    "end_date": graphene.String(),
    "db_id": graphene.String(),
    "provider_id": graphene.String(),
    "check_number": graphene.Int(),  # TODO: update data source to string...
    "covers": graphene.Int(),
    "total_paid_minimum": graphene.Float(),
    "total_paid_maximum": graphene.Float(),
}


class ChecksPage(graphene.ObjectType):
    checks = graphene.List(Check, **arguments)
    last_check_id = graphene.String()


class Query(object):
    checks = graphene.List(Check, **arguments)
    # checks = graphene.Field(ChecksPage, **arguments) # TODO: add paging support
    count = graphene.Int(**arguments)

    def resolve_checks(self, info, venue_id):
        checks = VenueDatabase(venue_id).retrieve_checks()
        return checks
        # TBD to paging implementation
        # return ChecksPage(checks=checks, last_check_id=last_check_id)

    def resolve_count(self, info, venue_id):
        return VenueDatabase(venue_id).retrieve_check_count()
