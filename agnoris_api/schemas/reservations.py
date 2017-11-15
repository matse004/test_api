import graphene

from storage.core.venue.database import VenueDatabase


class Guest(graphene.ObjectType):
    db_id = graphene.String()
    provider_id = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email_address = graphene.String()
    mobile_number = graphene.String()
    date_created = graphene.String()
    date_updated = graphene.String()
    last_visit = graphene.String()
    guest_notes = graphene.String()
    reservation_count = graphene.Int()
    cancellation_count = graphene.Int()
    no_show_count = graphene.Int()
    is_vip = graphene.Boolean()
    guest_tags = graphene.String()


class Reservation(graphene.ObjectType):
    db_id = graphene.String()
    provider_id = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email_address = graphene.String()
    mobile_number = graphene.String()
    date_booked = graphene.String()
    date_created = graphene.String()
    date_updated = graphene.String()
    cancelled = graphene.Boolean()
    cancelled_time = graphene.String()
    reservation_status = graphene.String()
    table_finished_time = graphene.String()
    table_seated_at = graphene.String()
    table_seated_time = graphene.String()
    table_type = graphene.String()
    covers = graphene.Int()
    server = graphene.String()
    visit_notes = graphene.String()
    visit_tags = graphene.String()
    is_walkin = graphene.Boolean()
    source_id = graphene.String()
    venue = graphene.String()


arguments = {
    "venue_id": graphene.String(),
    "limit": graphene.Int(),
    "first_name": graphene.String(),
    "last_name": graphene.String(),
    "start_date": graphene.String(),
    "end_date": graphene.String(),
    "db_id": graphene.String(),
    "provider_id": graphene.String(),
    "is_walkin": graphene.Boolean(),
    "cancelled": graphene.Boolean(),
    "covers": graphene.Int(),
    "email_address": graphene.String(),
    "mobile_number": graphene.String(),
    "source_id": graphene.String(),
}


class Query(object):
    reservations = graphene.List(Reservation, **arguments)
    guests = graphene.List(Guest)

    def resolve_reservations(self, args, venue_id):
        reservations = VenueDatabase(venue_id).retrieve_reservations()
        return reservations

