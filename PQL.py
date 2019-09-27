import time
import requests  # Install this if you don't have it already.
import datetime

PROMETHEUS = 'http://prometheus.my-clusterapps.corp.local/'

def mainloop():
# Midnight at the end of the previous month.
    currentDT = datetime.datetime.now()
    end_of_month = datetime.datetime.today().replace(day=1).date()
    # Last day of the previous month.
    last_day = end_of_month - datetime.timedelta(days=1)
    duration = '[' + str(last_day.day) + 'd]'
    while True:
    #'query': 'sum by (job)(increase(process_cpu_seconds_total' + duration + '))',
        response = requests.get(PROMETHEUS + '/api/v1/query',
        params={ 'query': '1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))'})
        results = response.json()

    #print('{:%B %Y}:'.format(value))
    #for result in results:
     # print(' {metric}: {value[1]}'.format(**result))
    #while True:
        print (results)
        print ("Current Second is: %d" % currentDT.second)
        time.sleep(3)
if __name__== "__main__":
    mainloop()
