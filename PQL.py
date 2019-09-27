import time
import requests  # Install this if you don't have it already.
import datetime
import json

PROMETHEUS = 'http://prometheus.my-clusterapps.corp.local/'

'''
d = """{"Aa": 1, "BB": "blabla", "cc": "False"}"""

d1 = json.loads(d)              # Produces a dictionary out of the given string
d2 = json.dumps(d)              # Produces a string out of a given dict or string
d3 = json.dumps(json.loads(d))  # 'dumps' gets the dict from 'loads' this time
'''

def mainloop():

    while True:
    #'query': 'sum by (job)(increase(process_cpu_seconds_total' + duration + '))',
        response = requests.get(PROMETHEUS + '/api/v1/query',
        params={ 'query': '1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))'})
        ### {"status":"success","data":{"resultType":"vector","result":[{"metric":{},"value":[1569619322.177,"0.6342261002060954"]}]}}
        results = json.loads(response.text)
        ###{u'status': u'success', u'data': {u'resultType': u'vector', u'result': [{u'metric': {}, u'value': [1569619322.177, u'0.6342261002060954']}]}}
        # 1. Test if response body contains sth.
        if results:
            # ...
            print("response text entered ")
        # 2. Handle error if deserialization fails (because of no text or bad format)
        try:
            ##responses = response.json()
            metricdict = results['data']
            # ...
        except ValueError:
            # no JSON returned
            print("no JASON returned")
            print("waiting 10 secs")
            time.sleep(10)
        else:

            print("^^^^^^^^^")
            print(results.keys())
            ##[u'status', u'data']
            print("^^^^^^^^^")
            ## ..///metricdict = results['data']
            print(metricdict.keys())
            #[u'resultType', u'result']
            cpumetric = metricdict['result']
            ##{u'metric': {}, u'value': [1569622615.046, u'0.6176136522020318']}
            print("$$$$")
            try:
                cpuavg =  cpumetric[0]
                print("rrr=" + str(cpuavg['value']))
            except IndexError:
                pass
            continue
                ##rrr=[1569623191.881, u'0.6377711405523562']
            cpuutil = cpuavg['value'][1]
                print("$$$$==" + str(cpuutil))
            ## $$$$==0.689901996444132
            currentDT = datetime.datetime.now()
            print ("Current Second is: %d" % currentDT.second)
        time.sleep(3)
if __name__== "__main__":
    mainloop()
