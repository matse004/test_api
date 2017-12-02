import graphene

from storage.core.reports.database import ReportsDatabase
from .scalars import JSONObjectString

arguments = {
    "venue_id": graphene.String(),
    "limit": graphene.Int(),
    "start_date": graphene.String(),
    "end_date": graphene.String(),
}


class Query(object):
    insights = JSONObjectString(**arguments)
    snapshots = JSONObjectString(**arguments)

    def resolve_insights(self, args, venue_id):
        insights = ReportsDatabase(venue_id).retrieve_insights()
        insights.pop("_id")
        return insights

    def resolve_snapshots(self, args, venue_id):
        snapshots = ReportsDatabase(venue_id).retrieve_snapshot()
        snapshots.pop("_id")
        return snapshots
