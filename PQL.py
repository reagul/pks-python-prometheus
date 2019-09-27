import time
import requests  # Install this if you don't have it already.
import datetime
import json

PROMETHEUS = 'http://prometheus.my-clusterapps.corp.local/'


def mainloop():

    while True:
    #'query': 'sum by (job)(increase(process_cpu_seconds_total' + duration + '))',
        response = requests.get(PROMETHEUS + '/api/v1/query',
        params={ 'query': '1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))'})
        print("#####")
        print(response.text)
        print("##########")
        ##results = response.json()
        results = json.loads(response.text)
        print (results)
        print("!!!!!!!!!!")
        currentDT = datetime.datetime.now()
        print ("Current Second is: %d" % currentDT.second)
        time.sleep(3)
if __name__== "__main__":
    mainloop()
