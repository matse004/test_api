# import graphene
#
# from storage.core import DashboardStorage
#
#
# class DateAccumulated(graphene.ObjectType):
#     year = graphene.Int()
#     month = graphene.Int()
#     day = graphene.Int()
#     covers = graphene.Int()
#     revenue = graphene.Float()
#
#
# def result_to_dateaccumulated(result):
#     return DateAccumulated(year=result["_id"].get("year"),
#                            month=result["_id"].get("month"),
#                            day=result["_id"].get("day"),
#                            covers=result.get("covers"),
#                            revenue=result.get("revenue"))
#
#
# def results_to_dateaccumulated_array(results):
#     date_accumulated = []
#     for result in results:
#         day_accumulated = result_to_dateaccumulated(result)
#         date_accumulated.append(day_accumulated)
#     return date_accumulated
#
# arguments = {
#     "limit": graphene.Int(),
#     "start_date": graphene.String(),
#     "end_date": graphene.String(),
# }
#
#
# class Query(graphene.AbstractType):
#     cover_by_day = graphene.List(DateAccumulated)
#     cover_by_week = graphene.List(DateAccumulated)
#     revenue_by_day = graphene.List(DateAccumulated)
#     revenue_by_week = graphene.List(DateAccumulated)
#     revenue_by_month = graphene.List(DateAccumulated)
#     snapshot_daily = graphene.List(DateAccumulated, **arguments)
#     snapshot_monthly = graphene.List(DateAccumulated, **arguments)
#
#     def resolve_cover_by_day(self,args, context, info):
#         days = DashboardStorage().get_cover_by_day()
#         return results_to_dateaccumulated_array(days)
#
#     def resolve_cover_by_week(self,args, context, info):
#         weeks = DashboardStorage().get_cover_by_week()
#         return results_to_dateaccumulated_array(weeks)
#
#     def resolve_revenue_by_day(self,args, context, info):
#         days = DashboardStorage().get_revenue_by_day()
#         return results_to_dateaccumulated_array(days)
#
#     def resolve_revenue_by_week(self,args, context, info):
#         weeks = DashboardStorage().get_revenue_by_week()
#         return results_to_dateaccumulated_array(weeks)
#
#     def resolve_revenue_by_month(self,args, context, info):
#         months = DashboardStorage().get_revenue_by_month()
#         return results_to_dateaccumulated_array(months)
#
#     def resolve_snapshot_daily(self, args, context, info):
#         snapshot = DashboardStorage().get_snapshot_by_day(args)
#         return results_to_dateaccumulated_array(snapshot)
#
#     def resolve_snapshot_monthly(self, args, context, info):
#         snapshot = DashboardStorage().get_snapshot_by_month(args)
#         return results_to_dateaccumulated_array(snapshot)
