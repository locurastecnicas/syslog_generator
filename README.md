# Syslog_generator

Generador de entradas para syslog/rsyslog. 
Permite especificar la prioridad, origen, delay entre entradas y tipo de entrada de syslog. Se distinguen los siguientes tipos de entradas:

* TEMP, para simular entradas syslog procedentes de un sensor de temperatura o monitor ambiental.
* MAIL, para simular entradas syslog generadas por un MTA. Se generan direcciones de remitente y destino aleatorias, asi como el subject.
* FIXED, para generar entradas con formato fijo en syslog.

Para los tipos MAIL y TEMP se generan diferentes campos de forma aleatoria para agregar mas informacion a cada entrada de syslog.


## Usando syslog_generator

Cuando se ejecuta sin argumentos utiliza la siguiente configuración por defecto:
* delay = 1 segundo
* facility = DAEMON
* priority = INFO
* logtype = FIXED

```
./syslog_generator.py
```
Para obtener ayuda, utilizar el argumento --help:

```
./syslog_generator --help
```
Para obtener ejemplos de uso, utilizar el argumento --examples:

```
./syslog_generator --help
```
