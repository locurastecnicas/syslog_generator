#!/usr/bin/python

import time
import sys
import syslog
import signal
import uuid
import random
import string

## Variables globales.
LOG_CONSTANTS={
  "LOG_KERN": syslog.LOG_KERN,
  "LOG_USER": syslog.LOG_USER,
  "LOG_MAIL": syslog.LOG_MAIL,
  "LOG_DAEMON": syslog.LOG_DAEMON,
  "LOG_AUTH": syslog.LOG_AUTH,
  "LOG_LPR": syslog.LOG_LPR,
  "LOG_NEWS": syslog.LOG_NEWS,
  "LOG_UUCP": syslog.LOG_UUCP,
  "LOG_CRON": syslog.LOG_CRON,
  "LOG_SYSLOG": syslog.LOG_SYSLOG,
  "LOG_LOCAL0": syslog.LOG_LOCAL0,
  "LOG_LOCAL1": syslog.LOG_LOCAL1,
  "LOG_LOCAL2": syslog.LOG_LOCAL2,
  "LOG_LOCAL3": syslog.LOG_LOCAL3,
  "LOG_LOCAL4": syslog.LOG_LOCAL4,
  "LOG_LOCAL5": syslog.LOG_LOCAL5,
  "LOG_LOCAL6": syslog.LOG_LOCAL6,
  "LOG_LOCAL7": syslog.LOG_LOCAL7,
  "LOG_EMERG": syslog.LOG_EMERG,
  "LOG_ALERT": syslog.LOG_ALERT,
  "LOG_CRIT": syslog.LOG_CRIT,
  "LOG_ERR": syslog.LOG_ERR,
  "LOG_WARNING": syslog.LOG_WARNING,
  "LOG_NOTICE": syslog.LOG_NOTICE,
  "LOG_INFO": syslog.LOG_INFO,
  "LOG_DEBUG": syslog.LOG_DEBUG
}

class syslog_entry:
  def __init__(self, secsdelay, logfacility, logpriority, entry_uuid, entry_type):
    self.delay=secsdelay
    self.facility=logfacility
    self.priority=logpriority
    self.uuid=entry_uuid
    self.logtype=entry_type

  def printConfig(self):
    print("Using the following configuration:")
    print(" delay => " + str(self.delay) + " secs")
    print(" priority => " + str(self.priority))
    print(" facility => " + str(self.facility))
    print(" logtype => " + str(self.logtype).upper())
    print("============================")

def control_signal(signal_control,signal_handler):
  print("Parando el generador de logs.")
  syslog.closelog()
  sys.exit()

def randomEmail():
  email_domains=("@gmail.com","@yahoo.com","@microsoft.com","@msn.com","@freemail.org","@mailfree.net","@notsofreemail.com","@wannadoo.es","@terra.es","@auna.com","@madritel.es","@yourmail.net")
  email_name="".join(random.sample(string.ascii_letters,5))

  return(email_name+"@"+email_domains[random.randint(0,len(email_domains)-1)])

def parseArgs(arguments):
  if (" ".join(arguments)).lower().find("help") != -1 or 1<=len(arguments)<3:
    print("")
    print(" -----------------------")
    print(" syslog_generator - v1.0")
    print(" -----------------------")
    print(" Generate syslog entries of different types and information.")
    print(" If invoked without arguments the default configuration assumed is:")
    print(" delay = 1 sec.")
    print(" facility = LOG_DAEMON")
    print(" priority = LOG_INFO")
    print("============================")
    print(" At least three arguments are required:")
    print("  --delay=N => Number of seconds between entries.")
    print("  --facility=FACILITY => Syslog facility used. Could be LOG_KERN, LOG_USER, LOG_MAIL, LOG_DAEMON, LOG_AUTH, LOG_LPR, LOG_NEWS, LOG_UUCP, LOG_CRON, LOG_SYSLOG and LOG_LOCAL0 to LOG_LOCAL7.")
    print("  --piority=PRIORITY => Syslog priority of mesages. Could be LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, LOG_NOTICE, LOG_INFO, LOG_DEBUG.")
    print("  --type=TYPE => Log entry to simulate. Could be TEMP(temperature sensor), MAIL(MTA mail flow), FIXED(fixed string).")
    print("  --help Print this screen")
    sys.exit(0)

  if len(arguments) == 0:
    config={
      "delay": 1,
      "facility": syslog.LOG_DAEMON,
      "priority": syslog.LOG_INFO,
      "type": "FIXED"
    } 
  else:
    config={}
    for argumentStr in arguments:
      tempStr=argumentStr.lower().strip("--")
      tempTuple=tempStr.partition("=")
      if tempTuple[0] == "facility" or tempTuple[0] == "priority":
        config[tempTuple[0]]=LOG_CONSTANTS[tempTuple[2].upper()]
      else:
        config[tempTuple[0]]=tempTuple[2]

  return(config)

def main():

  signal.signal(signal.SIGINT, control_signal)
  configValues=parseArgs(sys.argv[1:(len(sys.argv))])

  logaction=syslog_entry(configValues["delay"],configValues["facility"],configValues["priority"],uuid.uuid4(),configValues["type"])

  logaction.printConfig()

  syslog.openlog(logoption=syslog.LOG_PID,facility=logaction.facility)
  while 1:
    time.sleep(int(logaction.delay))
    infodate=time.ctime(time.time())
    if logaction.logtype.upper() == "MTA":
      syslogline="%s - Mail event <message_uid=%s> <size=%s Kbs> <mail_subject=%s> <mail_sender=%s> <destination_address=%s>"
      print(syslogline%(infodate,uuid.uuid4(),random.randint(1,100000),logaction.uuid,randomEmail(),randomEmail()))
      syslog.syslog(logaction.priority,syslogline%(infodate,uuid.uuid4(),random.randint(1,100000),logaction.uuid,randomEmail(),randomEmail()))
    elif logaction.logtype.upper() == "TEMP":
      syslogline="%s - Temperature %.2f - sensor ID %s"
      tValue=random.uniform(0,100)
      print(syslogline%(infodate,tValue,logaction.uuid))
      syslog.syslog(logaction.priority,syslogline%(infodate,tValue,logaction.uuid))
    else:
      syslogline="%s - Linea de syslog %s"
      print(syslogline%(infodate,logaction.uuid))
      syslog.syslog(logaction.priority,syslogline%(infodate,logaction.uuid))


## Inicio programa principal.
if __name__ == '__main__':
  main()
