from jsonpath_ng import parse
from .paginate import cw_paginate

from datetime import datetime as dt
from datetime import timedelta as td

#####################################

class get_metric_data(cw_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('MetricDataResults[*]')

#####################################

def _get_metric_stat(**kargs):

  ss = kargs.get('session')
  p = kargs.get('Period')
  mn = kargs.get('MetricName')
  s = kargs.get('Stat')
  u = kargs.get('Unit')
  ns = f"AWS/{kargs.get('Namespace')}"
  d = kargs.get('Dimensions')
  et = dt.now()
  st = et - td(days=kargs.get('days'))

  try:
      md = ss.client('cloudwatch').get_metric_statistics(StartTime=st, EndTime=et, 
                                                        Namespace=ns,
                                                        MetricName=mn,
                                                        Dimensions=[d],
                                                        Period=p, 
                                                        Statistics=[s])
      return md['Datapoints'][0][s] if len(md['Datapoints']) > 0 else None
  except Exception as e:
        print(e)
        return None

#####################################
# Utility
#####################################

def _get_metric_data(**kargs):

  ss = kargs.get('session')
  p = kargs.get('Period')
  mn = kargs.get('MetricName')
  s = kargs.get('Stat')
  u = kargs.get('Unit')
  ns = f"AWS/{kargs.get('Namespace')}"
  d = kargs.get('Dimensions')
  et = dt.now()
  st = et - td(days=kargs.get('days'))
  f = kargs.get('field')

  try:
      md = get_metric_data(ss, 
                              fields=[f], 
                              StartTime=st, 
                              EndTime=et, 
                              MetricDataQueries=[
                                  {"Id": "m1", 
                                   "MetricStat": {
                                       "Metric": {
                                           "Namespace": ns,
                                           "MetricName": mn,
                                           "Dimensions": [d]
                                       },
                                       "Period": p, 
                                       "Stat": s,
                                       "Unit": u
                                   }
                                  }
                              ]).json;
      return [m[f] if f in m and m[f] else None for m in md][0]
  except Exception as e:
        print(e)
        return None