import time
import requests  # Install this if you don't have it already.
import datetime
import json
import subprocess
import shlex
import re
import operator
import logging
import os
from subprocess import Popen,PIPE

PROMETHEUS = 'http://prometheus.my-clusterapps.corp.local/'
nodescalerlogfile = 'NodeScaler.txt'


def mainloop():

    ## Create the NodeLogger file
    logFileCreate()
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
            logFileWriter('INFO',"^^^^start loop^^^^^^^^^")
            print("STATUS:" + "PROMQL API Response Status =" + str(response.status_code))
            logFileWriter('INFO',"PROMQL API Response Status =" + str(response.status_code))
            results = json.loads(response.text)
            metricdict = results['data']
            # ...
        except ValueError, e:
            # no JSON returned
            ## possible 502 error
            print("sleep 20 secs VALUEERROR:" + str(e))
            logFileWriter('WARN',str(e))
            ## fall to secondary metric from METRIC_SERVER
            time.sleep(20)
            pass

        else:

            cpumetric = metricdict['result']
            ##{u'metric': {}, u'value': [1569622615.046, u'0.6176136522020318']}
            try:
                cpuavg =  cpumetric[0]
                ##rrr=[1569623191.881, u'0.6377711405523562']
                #print("rrr=" + str(cpuavg['value']))
                cpuutil = cpuavg['value'][1]
                cpupercent = (float(cpuutil))
                cpufinal = int(round(cpupercent,2) * 100)
                print("CPU-UTIL % ==" + str(cpufinal))
                logFileWriter('INFO',"CPU-UTIL % ==" + str(cpufinal))
                if cpufinal > 50 :
                    ##print("CPU util over 75 so sleep for 1mins")
                    ##time.sleep(60)
                    print("INFO: kickoff node creation + Sleep 10 min")
                    logFileWriter('INFO','Nodecreation kickoff')
                    workernodes = pksnodecreate()
                    print("INFO: WORKER NODES:=" + str(workernodes))
                    logFileWriter('INFO','Updated WorkerNodes Count=' + str(workernodes))
                    logFileWriter('INFO','SLEEP 10 minutes')
                    time.sleep(600)
            except IndexError:
                print("INDEXERROR: waiting 3 Minutes")
                logFileWriter('WARN','INDEXERROR: Sleeping 3 minutes')
                time.sleep(180)
                pass
            else:
            ## $$$$==0.689901996444132
                currentDT = datetime.datetime.now()
                print ("Current Second is: %d" % currentDT.second)


def pksnodecreate():

#def pksnodecreate():
   ## REad the curre
    args = ("pks","login","-a","pks.corp.local","-u","pksadmin","-k","-p","VMware1!")
    try:

        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        ##pks resize CLUSTER-NAME --num-nodes NUMBER-OF-WORKER-NODES
    except subprocess.CalledProcessError:
        print("Error Occured" + output)
        logFileWriter('WARN','Error Occured' + output)
    pksPrenodes = "pks cluster my-cluster"
    try:
        popen = subprocess.Popen(shlex.split(pksPrenodes), stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        clusterdict = str(output)
        clusternodes = clusterdict.strip().splitlines()
        #print(len(clusternodes))
        one,four,eight=operator.itemgetter(1,4,8)(clusternodes)
        #print(one,four,eight)
        ###
        ### AUTO adding 1 more node each time THIS loop is called
        workernodes = eight.split(':')
        presentworkernodeNumber = workernodes[1].strip()
        print(presentworkernodeNumber)
        scaleWorkerNodeNumber = int(float(presentworkernodeNumber)) + 1
        print(scaleWorkerNodeNumber)
        print("INFO: scaleWorkerNodeNumber:" + str(scaleWorkerNodeNumber))
        logFileWriter('INFO','New Scale Updated Nodes Count=' + str(scaleWorkerNodeNumber))
        if ( int(scaleWorkerNodeNumber) < int(presentworkernodeNumber) ):
            print("WARN: scaling Down..new scale:" + str(scaleWorkerNodeNumber) + " is less then Present scale: " + str(presentworkernode))
            logFileWriter('WARN',"Saling Down..new scale:" + str(scaleWorkerNodeNumber) + " is less then Present scale: " + str(presentworkernode))
        if ( int(scaleWorkerNodeNumber) == int(presentworkernodeNumber) ):
            print("WARN: Cluster is already at the same scale nothing to do here..returning empty")
            logFileWriter('WARN','Cluster is already at the same scale nothing to do here..returning empty')
            return scaleWorkerNodeNumber

    except subprocess.CalledProcessError:
        print("Error Occured" + output)
        logFileWriter('WARN','Error Occured' + output)
    #nodeargs = ("pks","resize","my-cluster","--num-nodes=","4","--non-interactive")

    nodeargs = "pks resize my-cluster --num-nodes=" + str(scaleWorkerNodeNumber) + " --non-interactive"
    #nodeargs = ("pks resize my-cluster --num-nodes=3 --non-interactive")
    try:

        popen = Popen(shlex.split(nodeargs), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print("COMMAND ISSUED " + str(nodeargs))
        logFileWriter('INFO','COMMAND ISSUED:=' + str(nodeargs))
        popen.wait()
        (stdout, stderr) = popen.communicate()
        #print("SHELL Output after create" + str(output))
        ##pks resize CLUSTER-NAME --num-nodes NUMBER-OF-WORKER-NODES
    except subprocess.CalledProcessError:
        print("Error Occured" + output)
        logFileWriter('WARN','Error Occured' + output)
    return scaleWorkerNodeNumber

def logFileCreate():

    if os.path.exists(nodescalerlogfile):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

        nodelog = open(nodescalerlogfile,append_write)
        nodelog.write("INFO: File ready for Logging NodeScaler \n")
        nodelog.close()

def logFileWriter(infolevel,message):

    ## https://docs.python.org/2.4/lib/minimal-example.html
    logging.basicConfig(level=logging.INFO,
                    format ='%(asctime)s %(levelname)s %(message)s',
                    filename = nodescalerlogfile ,
                    filemode ='w')


    if infolevel == 'DEBUG' :
        logging.debug(message)
    elif infolevel == 'INFO' :
        logging.info(message)
    elif infolevel == 'WARN' :
        logging.warning(message)
    else:
        logging.warn(message)


if __name__== "__main__":
    mainloop()
