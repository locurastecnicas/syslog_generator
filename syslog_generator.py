#!/usr/bin/python

import time
import sys
import syslog
import signal

class syslog_entry:
  def __init__(self, secsdelay, logfacility, logpriority):
    self.delay=secsdelay
    self.facility=logfacility
    self.priority=logpriority

  def printConfig(self):
    print("Using the following configuration:")
    print(" delay = " + str(self.delay) + " secs")
    print(" priority " + str(self.priority))
    print(" facility " + str(self.facility))

def control_signal(signal_control,signal_handler):
  print("Parando el generador de logs.")
  syslog.closelog()
  sys.exit()

def parseArgs(arguments):
  if (" ".join(arguments)).lower().find("help") != -1 or 1<len(arguments)<3:
    print("")
    print(" syslog_generator - v1.0")
    print(" -----------------------")
    print(" Generate syslog entries of different types and information.")
    print(" If invoked without arguments the default configuration assumed is:")
    print(" delay = 1 sec.")
    print(" facility = LOG_INFO")
    print(" priority = LOG_DAEMON")
    print("============================")
    print(" At least three arguments are required:")
    print("  --delay=N => Number of seconds between entries.")
    print("  --facility=FACILITY => Syslog facility used. Could be LOG_KERN, LOG_USER, LOG_MAIL, LOG_DAEMON, LOG_AUTH, LOG_LPR, LOG_NEWS, LOG_UUCP, LOG_CRON, LOG_SYSLOG and LOG_LOCAL0 to LOG_LOCAL7.")
    print("  --piority=PRIORITY => Syslog priority of mesages. Could be LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, LOG_NOTICE, LOG_INFO, LOG_DEBUG.")
    print("  --help Print this screen")
    sys.exit(0)

  if len(arguments) == 1:
    config={
      "delay": 1,
      "facility": syslog.LOG_INFO,
      "priority": syslog.LOG_DAEMON
    } 
    print("Using default configuration:")
    print(" delay = 1 sec.")
    print(" facility = LOG_INFO")
    print(" priority = LOG_DAEMON")
    print("============================")

  for argsStr in arguments:
    print("Parametro "+ argsStr)

  return(config)

def main():

  configValues={}
  signal.signal(signal.SIGINT, control_signal)
  configValues=parseArgs(sys.argv)

  logaction=syslog_entry(configValues["delay"],configValues["facility"],configValues["priority"])

  logaction.printConfig()
 
  syslog.openlog(logoption=syslog.LOG_PID,facility=logaction.facility)
  while 1:
    time.sleep(logaction.delay)
    infodate=time.ctime(time.time())
    syslogline="%s - Linea de syslog"
    print(syslogline%infodate)
    syslog.syslog(logaction.priority,syslogline%infodate)

if __name__ == '__main__':
  main()
