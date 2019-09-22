import datetime
import time
import requests  # Install this if you don't have it already.

PROMETHEUS = 'http://prometheus.my-clusterapps.corp.local/'

# Midnight at the end of the previous month.
end_of_month = datetime.datetime.today().replace(day=1).date()
# Last day of the previous month.
last_day = end_of_month - datetime.timedelta(days=1)
duration = '[' + str(last_day.day) + 'd]'

#'query': 'sum by (job)(increase(process_cpu_seconds_total' + duration + '))',
response = requests.get(PROMETHEUS + '/api/v1/query',
  params={ 'query': '1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))'})
results = response.json()

#print('{:%B %Y}:'.format(value))
#for result in results:
 # print(' {metric}: {value[1]}'.format(**result))
while True:
    print (results)
    time.sleep(3)

