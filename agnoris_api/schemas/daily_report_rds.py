import graphene
import json
from psycopg2 import pool
import logging
import datetime

from storage.core.RDS.rds import VenueReportingDb, DailyRepFields, RdsDB
from storage.utilities import get_env_variable
# from .scalars import JSONObjectString
from tivan.analysis.analyze_rds import VenueSnapshots

class DailyReportMetrics(graphene.Enum):
    ref_date = 'ref_date'
    prev_days = 'prev_days'
    prev_days_avg = 'prev_days_avg'
    same_days = 'same_days'
    same_days_avg = 'same_days_avg'
    WTD = 'wtd'
    MTD = 'mtd'
    YTD = 'ytd'
    party_size_grp = 'party_size_grp'
    mp_rc_grp = 'mp_rc_grp'
    rc_mp_grp = 'rc_mp_grp'
    top_items = 'top_items'
    top_items_by_party = 'top_items_by_party'
    top_items_pop = 'top_items_pop'
    labor_by_mp = 'labor_by_mp'
    labor_by_emp = 'labor_by_emp repeats'
    repeats = 'repeats'
    all_fields = '*'


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
    same_days_avg = graphene.Field(DailyMetrics)
    WTD = graphene.Field(DailyMetrics)
    MTD = graphene.Field(DailyMetrics)
    YTD = graphene.Field(DailyMetrics)

    party_size_grp = graphene.String()
    mp_rc_grp = graphene.String()
    rc_mp_grp = graphene.String()
    top_items = graphene.String()
    top_items_by_party = graphene.String()
    top_items_pop = graphene.String()
    labor_by_mp = graphene.String()
    labor_by_emp = graphene.String()
    repeats = graphene.String()

def results_to_prev_days_array(results):
    reports = []
    for result in results:
        report = load_list_of_daily_metrics(result)
        reports.append(report)
    return reports

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
            start_date=day.get(DailyRepFields.start_date)
            , end_date=day.get(DailyRepFields.end_date)
            , sales=day.get(DailyRepFields.sales)
            , covers=day.get(DailyRepFields.covers)
            , checks=day.get(DailyRepFields.checks)
            , avg_check=day.get(DailyRepFields.avg_check)
        ))
    return days

def rds_to_daily_report(result):
    report = DailyReport()

    if result.get(DailyRepFields.ref_date):
        report.date = result.get(DailyRepFields.ref_date)
    else:
        return

    if result.get(DailyRepFields.prev_days):
        prev_days = json.loads(result.get(DailyRepFields.prev_days))
        prev_days = load_list_of_daily_metrics(prev_days)
        report.prev_days = prev_days

    if result.get(DailyRepFields.prev_days_avg):
        avg = json.loads(result.get(DailyRepFields.prev_days_avg))
        prev_days_avg = DailyMetrics(
            start_date=avg.get(DailyRepFields.start_date)
            , end_date=avg.get(DailyRepFields.end_date)
            , sales=avg.get(DailyRepFields.sales)
            , covers=avg.get(DailyRepFields.covers)
            , checks=avg.get(DailyRepFields.checks)
            , avg_check=avg.get(DailyRepFields.avg_check)
        )
        report.prev_days_avg = prev_days_avg

    if result.get(DailyRepFields.same_days):
        same_days = json.loads(result.get(DailyRepFields.same_days))
        same_days = load_list_of_daily_metrics(same_days)
        report.same_days = same_days

    if result.get(DailyRepFields.same_days_avg):
        avg = json.loads(result.get(DailyRepFields.same_days_avg))
        same_days_avg = DailyMetrics(
            start_date=avg.get(DailyRepFields.start_date)
            , end_date=avg.get(DailyRepFields.end_date)
            , sales=avg.get(DailyRepFields.sales)
            , covers=avg.get(DailyRepFields.covers)
            , checks=avg.get(DailyRepFields.checks)
            , avg_check=avg.get(DailyRepFields.avg_check)
        )
        report.same_days_avg = same_days_avg

    if result.get(DailyRepFields.WTD):
        WTD = json.loads(result.get(DailyRepFields.WTD))
        WTD = DailyMetrics(
            start_date=WTD.get(DailyRepFields.start_date)
            , end_date=WTD.get(DailyRepFields.end_date)
            , sales=WTD.get(DailyRepFields.sales)
            , covers=WTD.get(DailyRepFields.covers)
            , checks=WTD.get(DailyRepFields.checks)
            , avg_check=WTD.get(DailyRepFields.avg_check)
        )
        report.WTD = WTD

    if result.get(DailyRepFields.MTD):
        MTD = json.loads(result.get(DailyRepFields.MTD))
        MTD = DailyMetrics(
            start_date=MTD.get(DailyRepFields.start_date)
            , end_date=MTD.get(DailyRepFields.end_date)
            , sales=MTD.get(DailyRepFields.sales)
            , covers=MTD.get(DailyRepFields.covers)
            , checks=MTD.get(DailyRepFields.checks)
            , avg_check=MTD.get(DailyRepFields.avg_check)
        )
        report.MTD = MTD

    if result.get(DailyRepFields.YTD):
        YTD = json.loads(result.get(DailyRepFields.YTD))
        YTD = DailyMetrics(
            start_date=YTD.get(DailyRepFields.start_date)
            , end_date=YTD.get(DailyRepFields.end_date)
            , sales=YTD.get(DailyRepFields.sales)
            , covers=YTD.get(DailyRepFields.covers)
            , checks=YTD.get(DailyRepFields.checks)
            , avg_check=YTD.get(DailyRepFields.avg_check)
        )
        report.YTD = YTD

    if result.get(DailyRepFields.party_size_grp):
        party_siz_grp = result.get(DailyRepFields.party_size_grp)
        report.party_size_grp = party_siz_grp

    if result.get(DailyRepFields.mp_rc_grp):
        mp_rc_grp = result.get(DailyRepFields.mp_rc_grp)
        report.mp_rc_grp = mp_rc_grp

    if result.get(DailyRepFields.rc_mp_grp):
        rc_mp_grp = result.get(DailyRepFields.rc_mp_grp)
        report.rc_mp_grp = rc_mp_grp

    if result.get(DailyRepFields.top_items):
        top_items = result.get(DailyRepFields.top_items)
        report.top_items = top_items

    if result.get(DailyRepFields.top_items_by_party):
        top_items_by_party = result.get(DailyRepFields.top_items_by_party)
        report.top_items_by_party = top_items_by_party

    if result.get(DailyRepFields.top_items_pop):
        top_items_pop = result.get(DailyRepFields.top_items_pop)
        report.top_items_pop = top_items_pop

    if result.get(DailyRepFields.labor_by_mp):
        labor_by_mp = result.get(DailyRepFields.labor_by_mp)
        report.labor_by_mp = labor_by_mp

    if result.get(DailyRepFields.labor_by_emp):
        labor_by_emp = result.get(DailyRepFields.labor_by_emp)
        report.labor_by_emp = labor_by_emp

    if result.get(DailyRepFields.repeats):
        repeats = result.get(DailyRepFields.repeats)
        report.repeats = repeats

    return report

arguments = {
    "venue_id": graphene.String(),
    "limit": graphene.Int(),
    "start_date": graphene.String(),
    "end_date": graphene.String(),
    "ref_date": graphene.String(),
    "fields_list": graphene.List(DailyReportMetrics),
    "force_calc_flg": graphene.Boolean(),
    "calc_new_flg": graphene.Boolean()
}


class Query(graphene.ObjectType):
    daily_reports = graphene.List(DailyReport, **arguments)

    def resolve_daily_reports(self, info, start_date, end_date, venue_id, fields_list=[DailyReportMetrics.all_fields.value], calc_new_flg=True, force_calc_flg=False):
        # filed_list = [field.values for field in fields_list_str]
        # fields_str = ', '.join(fields_list)
        conn=None
        if info.context:
            conn = info.context.get('rds_conn')

        # force_calc_flg = args.get('force_calc_flg')
        # venue_id = args.get('venue_id')
        # start_date = args.get('start_date')
        # end_date = args.get('end_date')
        # fields_list = args.get('fields_list')
        # calc_new_flg = args.get('calc_new_flg')

        if force_calc_flg:
            reports = VenueSnapshots(venue_id).save_stats_by_date(start_date, end_date, metrics_list=fields_list)
        else:
            reports = VenueReportingDb(venue_id, conn=conn).retrieve_report_data(start_date, end_date, fields_list=fields_list)

        # if no data in rds - try to calculate
        # TODO: add field list
        if not reports and calc_new_flg:
            reports = VenueSnapshots(venue_id).save_stats_by_date(start_date, end_date, metrics_list=fields_list)

        if reports:
            return results_to_daily_reports_array(reports)
        else:
            return None

schema = graphene.Schema(query=Query)
query = """
            query{
                dailyReports(startDate: "14/03/2018", endDate: "14/03/2018", venueId: "8962a8ff-d314-487d-9403-1897372cbd07")
                {
                    date
                }
                }
        """
query1 = """
            query{
                dailyReports(startDate: "12/03/2018", endDate: "12/03/2018", venueId: "8962a8ff-d314-487d-9403-1897372cbd07")
                {
                    date
                }
                }
        """


class RdsPool():
    def __init__(self):
        connection_string = str(get_env_variable("RDS_DWH_CONNECTION_STRING", exception_on_failure=True))

        try:
            self.conn_pool = pool.ThreadedConnectionPool(minconn=15, maxconn=100, dsn=connection_string)
        except Exception as ex:
            # self.LOGGER.error("Can't create connection pool: {}".format(str(ex)))
            print("Can't create connection pool")


if __name__ == '__main__':
    ts =  datetime.datetime.now()
    rds = RdsPool()
    te = datetime.datetime.now()
    print("pooling: {}".format(te-ts))

    ts =  datetime.datetime.now()
    conn = rds.conn_pool.getconn()
    result = schema.execute(query,  context_value={'rds_conn': conn})
    # print(result.data)
    rds.conn_pool.putconn(conn=conn)
    te = datetime.datetime.now()
    print("first query: {}".format(te-ts))

    # ts = datetime.datetime.now()
    # conn = rds.conn_pool.getconn()
    # result = schema.execute(query1, context_value={'rds_conn':conn})
    # # print(result.data)
    # rds.conn_pool.putconn(conn=conn)
    # te = datetime.datetime.now()
    # print("second query: {}".format(te-ts))




