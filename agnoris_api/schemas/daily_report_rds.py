import graphene
import json

from storage.core.RDS.rds import VenueReportingDb
from .scalars import JSONObjectString

class DailyMetrics(graphene.ObjectType):
    start_date = graphene.String()
    end_date = graphene.String()
    covers = graphene.Int()
    checks = graphene.Int()
    sales = graphene.Float()
    avg_check = graphene.Float()


class DailyReport(graphene.ObjectType):
    date = graphene.String()
    prev_days = graphene.List(DailyMetrics)
    prev_days_avg = graphene.Field(DailyMetrics)
    same_days = graphene.List(DailyMetrics)
    WTD = graphene.Field(DailyMetrics)
    party_size_grp = graphene.String()


def results_to_daily_reports_array(results):
    reports = []
    for result in results:
        report = rds_to_daily_report(result)
        reports.append(report)
    return reports

def load_list_of_daily_metrics(d):
    days=[]
    for day in d:
        days.append(DailyMetrics(
            start_date=day.get("check_open_date")
            , end_date=day.get("check_open_date")
            , sales=day.get("items_total")
            , covers=day.get("covers")
            , checks=day.get("checks_count")
            , avg_check=day.get("avg_check")
        ))
    return days

def rds_to_daily_report(result):
    report = DailyReport()

    # prev_days = None
    if result.get("prev_days"):
        prev_days = json.loads(result.get("prev_days"))
        prev_days = load_list_of_daily_metrics(prev_days)
        report.prev_days =prev_days

    # prev_days_avg = None
    if result.get("prev_days_avg"):
        avg = json.loads(result.get("prev_days_avg"))
        prev_days_avg = DailyMetrics(
            start_date=avg.get("start_date")
            , end_date=avg.get("end_date")
            , sales=avg.get("items_total")
            , covers=avg.get("covers")
            , checks=avg.get("checks_count")
            , avg_check=avg.get("avg_check")
        )
        report.prev_days_avg = prev_days_avg

    # party_size_grp = None
    if result.get("party_size_grp"):
        party_siz_grp = result.get("party_size_grp")
        report.party_size_grp = party_siz_grp

    # report = DailyReport(
    #     date = result.get("ref_date")
    #     , prev_days=prev_days
    #     , prev_days_avg = prev_days_avg
    #     , party_size_grp = party_siz_grp
    # )

    return report

arguments = {
    "venue_id": graphene.String(),
    "limit": graphene.Int(),
    "start_date": graphene.String(),
    "end_date": graphene.String(),
    "ref_date": graphene.String()
}


class Query(object):
    # daily_metrics = graphene.List(DailyMetrics, **arguments)
    daily_reports = graphene.List(DailyReport, **arguments)
    # snapshots = JSONObjectString(**arguments)

    def resolve_daily_reports(self, args, start_date, end_date, venue_id):
        reports = VenueReportingDb(venue_id).retrieve_report_data(start_date, end_date, fields_list_str='*')
        return results_to_daily_reports_array(reports)

