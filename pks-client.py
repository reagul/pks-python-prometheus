
import subprocess
##import subprocess
args = ("pks","login","-a","pks.corp.local","-u","pksadmin","-k","-p","VMware1!")
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output, err = popen.communicate()
exitcode = popen.returncode
print ("err" + err )
print ("out" + output)
print ("exitcode" + exitcode)
