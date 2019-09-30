import time
import requests  # Install this if you don't have it already.
import datetime
import json
import subprocess
from subprocess import Popen,PIPE

PROMETHEUS = 'http://prometheus.my-clusterapps.corp.local/'


def mainloop():

    while True:
    #'query': 'sum by (job)(increase(process_cpu_seconds_total' + duration + '))',
        response = requests.get(PROMETHEUS + '/api/v1/query',
        params={ 'query': '1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))'})
        ### {"status":"success","data":{"resultType":"vector","result":[{"metric":{},"value":[1569619322.177,"0.6342261002060954"]}]}}

        ###{u'status': u'success', u'data': {u'resultType': u'vector', u'result': [{u'metric': {}, u'value': [1569619322.177, u'0.6342261002060954']}]}}
        time.sleep(3)
        ## http://prometheus.my-clusterapps.corp.local/api/v1/query?query=1%20-%20avg(rate(node_cpu_seconds_total{mode=%22idle%22}[1m]))
        try:
            ##responses = response.json()
            print("^^^^^^^^^")
            print("STATUS:" + str(response.status_code))
            results = json.loads(response.text)
            metricdict = results['data']
            # ...
        except ValueError, e:
            # no JSON returned
            ## possible 502 error
            print("sleep 20 secs VALUEERROR:" + str(e))
            ## fall to secondary metric from METRIC_SERVER
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
                cpupercent = (float(cpuutil))
                cpufinal = int(round(cpupercent,2) * 100)
                if cpufinal > 75 :
                    print("kickoff node creation")
                    print("sleep for 10 mins")
                    pksnodecreate()
                    time.sleep(600)
            except IndexError:
                print("INDEXERROR: waiting 20 secs")
                time.sleep(20)
                pass
            else:
            ## $$$$==0.689901996444132
                currentDT = datetime.datetime.now()
                print ("Current Second is: %d" % currentDT.second)

def pksnodecreate():

    args = ("pks","login","-a","pks.corp.local","-u","pksadmin","-k","-p","VMware1!")
    try:

        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        ##pks resize CLUSTER-NAME --num-nodes NUMBER-OF-WORKER-NODES
    except subprocess.CalledProcessError:
        print("Error Occured" + output)

    args = ("pks","resize","my-cluster","--num-nodes","1")

    try:
        ## foo_proc = Popen(['ionic', 'cordova', 'prepare'], stdin=PIPE, stdout=PIPE)
        popen = Popen(args, stdin=PIPE, stdout=PIPE, shell=True)
        popen.wait()
        output = popen.stdout.read()
        popen.communicate(input='y')
        ##pks resize CLUSTER-NAME --num-nodes NUMBER-OF-WORKER-NODES
    except subprocess.CalledProcessError:
        print("Error Occured" + output)

if __name__== "__main__":
    mainloop()
