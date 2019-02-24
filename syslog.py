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
    print("Generando logs cada " + str(self.delay) + " segundos")
    print("Registrando logs con prioridad " + str(self.priority))
    print("Registrando logs con facility " + str(self.facility))

def control_signal(signal_control,signal_handler):
  print("Parando el generador de logs.")
  syslog.closelog()
  sys.exit()

def parseArgs(arguments):
  argsList={}
  for argsStr in arguments:
    print("Parametro "+ argsStr)

def main():

  signal.signal(signal.SIGINT, control_signal)
  parseArgs(sys.argv)

  sys.exit(0)

  if len(sys.argv) == 1:
    print("Los argumentos son: " + sys.argv[0])
    logaction=syslog_entry(1,syslog.LOG_DAEMON,syslog.LOG_INFO)
  else:
    logaction=syslog_entry(int(sys.argv[1]),syslog.LOG_DAEMON,syslog.LOG_INFO)

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
