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
        ### {"status":"success","data":{"resultType":"vector","result":[{"metric":{},"value":[1569619322.177,"0.6342261002060954"]}]}}

        ###{u'status': u'success', u'data': {u'resultType': u'vector', u'result': [{u'metric': {}, u'value': [1569619322.177, u'0.6342261002060954']}]}}
        time.sleep(3)
        try:
            ##responses = response.json()
            print("^^^^^^^^^")
            print("STATUS:" + str(response.status_code))
            results = json.loads(response.text)
            metricdict = results['data']
            # ...
        except ValueError, e:
            # no JSON returned
            print("EPRINTEF:" + str(e))
            print("ERROR1: waiting 20 secs")
            time.sleep(20)
            pass

        else:

            #print("^^^^^^^^^")
            #print(results.keys())
            ##[u'status', u'data']
            #print("^^^^^^^^^")
            ## ..///metricdict = results['data']
            #print(metricdict.keys())
            #[u'resultType', u'result']
            cpumetric = metricdict['result']
            ##{u'metric': {}, u'value': [1569622615.046, u'0.6176136522020318']}
            try:
                cpuavg =  cpumetric[0]
                ##rrr=[1569623191.881, u'0.6377711405523562']
                #print("rrr=" + str(cpuavg['value']))
                cpuutil = cpuavg['value'][1]

                print("$$$$==" + str(cpuutil))
                cpupercent = float(cpuutil) * 100
                print("Formatted: "+"{:.2%}".format(cpuutil));
            except IndexError:
                print("ERROR2: waiting 15 secs")
                time.sleep(15)
                pass
            else:
            ## $$$$==0.689901996444132
                currentDT = datetime.datetime.now()
                print ("Current Second is: %d" % currentDT.second)

if __name__== "__main__":
    mainloop()
