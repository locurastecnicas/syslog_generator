# Syslog_generator

Generador de entradas para syslog/rsyslog. 
Permite especificar la prioridad, origen, delay entre entradas y tipo de entrada de syslog. Se distinguen los siguientes tipos de entradas:

* TEMP, para simular entradas syslog procedentes de un sensor de temperatura o monitor ambiental.
* MAIL, para simular entradas syslog generadas por un MTA. Se generan direcciones de remitente y destino aleatorias, asi como el subject.
* FIXED, para generar entradas con formato fijo en syslog.

