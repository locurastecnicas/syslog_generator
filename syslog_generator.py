#!/usr/bin/python

import time
import sys
import syslog
import signal
import uuid
import random
import string
import threading

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

## Definicion clase syslog_entry.
class syslog_entry(threading.Thread):
  def __init__(self, secsdelay, logfacility, logpriority, entry_uuid, entry_type):
    threading.Thread.__init__(self)
    self.close_flag=threading.Event()
    self.delay=secsdelay
    self.facility=logfacility
    self.priority=logpriority
    self.uuid=entry_uuid
    self.logtype=entry_type
    self.sensorname=sensorName()
    self.sensorip=sensorIP()

  def printConfig(self):
    print("Using the following configuration:")
    print(" delay\t\t => " + str(self.delay) + " secs")
    print(" priority\t => " + str(self.priority))
    print(" facility\t => " + str(self.facility))
    print(" logtype\t => " + str(self.logtype).upper())
    print("============================")

  def run(self):
    syslog.openlog(logoption=syslog.LOG_PID,facility=self.facility)
    random.seed()
    baseTemperature=random.uniform(0,100)
    while not self.close_flag.is_set():
      time.sleep(int(self.delay))
      infodate=time.ctime(time.time())
      if self.logtype.upper() == "MAIL":
        syslogline="[SYSLOG_GEN] %s - Mail event <message_uid=%s> <size=%s Kbs> <mail_subject=%s> <mail_sender=%s> <destination_address=%s>"
        print(syslogline%(infodate,uuid.uuid4(),random.randint(1,100000),self.uuid,randomEmail(),randomEmail()))
        syslog.syslog(self.priority,syslogline%(infodate,uuid.uuid4(),random.randint(1,100000),self.uuid,randomEmail(),randomEmail()))
      elif self.logtype.upper() == "TEMP":
        syslogline="[SYSLOG_GEN] %s - <%s> Temperature %.2f - sensor ID %s sensor IP %s"
        random.seed()
        temperatureVar=random.uniform(0,10)
        print(syslogline%(infodate,self.sensorname,baseTemperature+temperatureVar,self.uuid,self.sensorip))
        syslog.syslog(self.priority,syslogline%(infodate,self.sensorname,baseTemperature+temperatureVar,self.uuid,self.sensorip))
      else:
        syslogline="[SYSLOG_GEN] %s - Syslog entry %s - SOURCE: %s"
        print(syslogline%(infodate,self.uuid,self.sensorip))
        syslog.syslog(self.priority,syslogline%(infodate,self.uuid,self.sensorip))

    print("Closing logger thread: " + str(self.uuid) + "Logger type: " + self.logtype)
    syslog.closelog()

def control_signal(signal_control,signal_handler):
  print("Stopping log generator. Please wait....")
  print("Signal received: " + str(signal_control))
  raise ExitProgram

def sensorName():
  names_list=("RACK","COMS_ROOM","SERVER","SERVERS_ROOM","DATACENTER_COOLING")

  random.seed()
  return(names_list[random.randint(0,len(names_list)-1)])

def sensorIP():
  ip_list=("172.22.254.1","172.22.254.10","172.22.254.20","172.22.254.30","172.22.254.40","172.22.254.50","172.22.254.60","172.22.254.7","172.22.254.70")

  random.seed()
  return(ip_list[random.randint(0,len(ip_list)-1)])

def randomEmail():
  email_domains=("@gmail.com","@yahoo.com","@microsoft.com","@msn.com","@freemail.org","@mailfree.net","@notsofreemail.com","@wannadoo.es","@terra.es","@auna.com","@madritel.es","@yourmail.net")
  email_name="".join(random.sample(string.ascii_letters,5))

  random.seed()
  return(email_name+"@"+email_domains[random.randint(0,len(email_domains)-1)])

class ExitProgram(Exception):
  pass

def parseArgs(arguments):
  if (arguments.lower().find("examples")) != -1:
    print("")
    print(" -----------------------")
    print(" syslog_generator - v1.0")
    print(" -----------------------")
    print(" Usage examples:")
    print("  - Generate fake temperature syslog entries every 5 seconds with LOG_KERN facility and LOG_CRIT priority.")
    print("     syslog_generator --delay=5,facility=LOG_KERN,priority=LOG_CRIT,type=TEMP")
    print("  - Generate fake temperature syslog entries every 5 seconds with LOG_KERN facility and LOG_CRIT priority and")
    print("    fixed syslog entries every 15 seconds with LOG_AUTH facility and LOG_INFO priority.")
    print("     syslog_generator --delay=5,facility=LOG_KERN,priority=LOG_CRIT,type=TEMP --delay=15,facility=LOG_AUTH,priority=LOG_INFO,type=FIXED")
    print("")
    sys.exit(0)

  if (arguments.lower().find("help")) != -1 or (arguments.count("=") % 2) != 0:
    print("")
    print(" -----------------------")
    print(" syslog_generator - v1.0")
    print(" -----------------------")
    print(" Generate syslog entries of different types and information.")
    print(" Every configuration entry defines a generator. The syntax is as follows:")
    print("   syslog_generator --GENERATOR1_CONFIG --GENERATOR2_CONFIG .... --GENERATORN_CONFIG") 
    print(" Four arguments are required for every GENERATOR_CONFIG separated by commas:")
    print("  delay=N\t\t => Number of seconds between entries.")
    print("  facility=FACILITY\t => Syslog facility used. Could be LOG_KERN, LOG_USER, LOG_MAIL, LOG_DAEMON, LOG_AUTH, LOG_LPR, LOG_NEWS, LOG_UUCP, LOG_CRON, LOG_SYSLOG and LOG_LOCAL0 to LOG_LOCAL7.")
    print("  piority=PRIORITY\t => Syslog priority of mesages. Could be LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, LOG_NOTICE, LOG_INFO, LOG_DEBUG.")
    print("  type=TYPE\t\t => Log entry to simulate. Could be TEMP(temperature sensor), MAIL(MTA mail flow), FIXED(fixed string).")
    print(" If you need help or want to check some examples try:")
    print("  --help\t\t => Print this screen.")
    print("  --examples\t\t => Print usage examples.") 
    print("")
    print(" Please note, if invoked without arguments the default configuration is:")
    print("  delay    = 1 sec.")
    print("  facility = LOG_DAEMON")
    print("  priority = LOG_INFO")
    print("  type     = FIXED")
    print("============================")
    print("")
    sys.exit(0)

  if (arguments.lower().find("default")) != -1:
    config={
      "delay": 1,
      "facility": syslog.LOG_DAEMON,
      "priority": syslog.LOG_INFO,
      "type": "FIXED"
    } 
  else:
    config={}
    tempStr=arguments.lower().strip("--")
    for keyPair in tempStr.split(','):
      tempTuple=keyPair.partition("=")
      if tempTuple[0] == "facility" or tempTuple[0] == "priority":
        config[tempTuple[0]]=LOG_CONSTANTS[tempTuple[2].upper()]
      else:
        config[tempTuple[0]]=tempTuple[2]

  return(config)

def main():

  try:
    signal.signal(signal.SIGINT, control_signal)
    signal.signal(signal.SIGTERM, control_signal)
   
    loggers_list=[]
    if (len(sys.argv)) == 1:
      configValues=parseArgs("DEFAULT")
      logaction=syslog_entry(configValues["delay"],configValues["facility"],configValues["priority"],uuid.uuid4(),configValues["type"])
      loggers_list.append(logaction)
      logaction.printConfig()
      logaction.start()
    else:
      for argumentStr in sys.argv[1:(len(sys.argv))]:
        configValues=parseArgs(argumentStr)
        logaction=syslog_entry(configValues["delay"],configValues["facility"],configValues["priority"],uuid.uuid4(),configValues["type"])
        loggers_list.append(logaction)
        logaction.printConfig()
        logaction.start()

    while True:
      time.sleep(0.5)

  except ExitProgram:
    for loggerThread in threading.enumerate():
      print("Thread: " + loggerThread.getName())

    print("Finishing logging operations.......")
    for logger in loggers_list:
      logger.close_flag.set()
      logger.join()

  print("Closing main program.")
  syslog.closelog()
  sys.exit()

## Inicio programa principal.
if __name__ == '__main__':
  main()
