# import graphene
# from bson.json_util import dumps
#
# from storage.core import DashboardStorage
#
#
# class Query(graphene.AbstractType):
#     report_json = graphene.String()
#
#     def resolve_report_json(self,args, context, info):
#         report = DashboardStorage().get_latest_analysis_report()
#         report_json = dumps(report)
#         return report_json
