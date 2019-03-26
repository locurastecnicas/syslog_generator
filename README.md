# Syslog_generator

Generador de entradas aleatorias para syslog/rsyslog. Pensado para generar trafico desde maquinas UNIX/LINUX a centralizadores de logs y pruebas de carga. 
Permite especificar la prioridad, origen, delay entre entradas y tipo de entrada de syslog. Se distinguen los siguientes tipos de entradas:

* TEMP, para simular entradas syslog procedentes de un sensor de temperatura o monitor ambiental.
* MAIL, para simular entradas syslog generadas por un MTA. Se generan direcciones de remitente y destino aleatorias, asi como el subject.
* FIXED, para generar entradas con formato fijo en syslog.

Para los tipos MAIL y TEMP se generan diferentes campos de forma aleatoria para agregar mas informacion a cada entrada de syslog.
Cada tipo de logger se lanza en un thread individual, con lo que es posible registrar cada entrada en diferentes ficheros de log de manera simultanea y
simular flujos de log diferentes para sistemas como Elasticsearch mediante filebeat.

## Requisitos

Syslog_generator esta programado en Python, con lo que solo es necesario tener instalada una version de Python 2.7.12 o superior.

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
./syslog_generator.py --help
```
Para obtener ejemplos de uso, utilizar el argumento --examples:

```
./syslog_generator.py --examples
```
Para generar entradas simulando un flujo de correos cada 20 segundos, con prioridad WARNING y registrandolo con la facility LOG_MAIL, la ejecucion del comando podria ser:

```
./syslog_generator.py --delay=20,priority=LOG_WARNING,facility=LOG_MAIL,type=MAIL
```
Con el comando anterior se crearia un thread que realizaria el registro con el tipo de entrada indicada en syslog.

En caso de querer generar varios registros de manera simultanea, por ejemplo el flujo de correos anterior y adicionalmente simular un sensor de temperatura, con un intervalo
entre registros de 5 segundos, la ejecucion del comando seria como la siguiente:

```
./syslog_generator.py --delay=20,priority=LOG_WARNING,facility=LOG_MAIL,type=MAIL --delay=5,priority=LOG_INFO,facility=LOG_SYSLOG,type=TEMP
```
