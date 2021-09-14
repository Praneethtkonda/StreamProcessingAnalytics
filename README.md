# Intelligent Vehicle Monitoring System
Prepare a working prototype of this IVMS using open source messaging platform Apache Kafka. A working prototype should mimic the following requirements -
1)	Capturing the real time truck movement data from the sensors fitted in the trucks
2)	Moving the running truck data over MQTT protocol to a centralized location
3)	Moving data from centralized location to messaging store for intermittent storage (may put it in the persistent storage as well)
4)	Preprocessing of the data received from the trucks for quality checks and for other required transformations
5)	Doing the processing of data to identify the drivers exceeding the speed limits
6)	Providing a mechanism to flag out the details of drivers exceeding the speed limits
7)	Providing a way to maintain the count of over speeding incidents over the period of time, on particular routes, for particular trucks etc.

## Our Architecture
![`Architecture`](Kafka.drawio.png)
Refer to the [recorded video](https://drive.google.com/file/d/1zyNgvYWL44D9qsNQY0Zb8VdanB0iLWO1/view?usp=sharing) for more clarification on the architecture.

## Running your mosquitto client
For windows
```
PS Y:\git\spa> py -m venv env
PS Y:\git\spa> .\env\Scripts\activate
(env) PS Y:\git\spa> pip install -r requirements.txt
(env) PS Y:\git\spa> python mqtt_client_data_gen.py
```
For Linux
```bash
root@user$ python3 -m venv env
root@user$ source env/bin/activate
(env) root@user/spa/$ pip install -r requirements.txt
(env) root@user/spa/$ python mqtt_client_data_gen.py
```

## Running the development environment
Bring up the set of containers will bring up the whole pipeline for stream processing and analytics.

```
PS Y:\git\spa> docker-compose up
n confluent_rmoff_01ksql_processing_log-0 in response to UpdateMetadata request sent by controller 1 epoch 1 with correlation id 4 (state.change.logger)
kafka             | [2021-08-18 12:20:01,840] INFO [Broker id=1] Add 1 partitions and deleted 0 partitions from metadata cache in response to UpdateMetadata request sent by controller 1 epoch 1 with correlation id 4 (state.change.logger)
kafka             | [2021-08-18 12:20:01,841] TRACE [Controller id=1 epoch=1] Received response UpdateMetadataResponseData(errorCode=0) for request UPDATE_METADATA with correlation id 4 sent to broker kafka:29092 (id: 1 rack: null) (state.change.logger)
ksqldb            | [2021-08-18 12:20:01,868] INFO Reading prior command records up to offset 0 (io.confluent.ksql.rest.server.CommandTopic:112)
ksqldb            | [2021-08-18 12:20:01,878] INFO Restoring previous state from 0 commands. (io.confluent.ksql.rest.server.computation.CommandRunner:257)
ksqldb            | [2021-08-18 12:20:01,878] INFO Restarting 0 queries. (io.confluent.ksql.rest.server.computation.CommandRunner:287)
ksqldb            | [2021-08-18 12:20:01,880] INFO Restore complete (io.confluent.ksql.rest.server.computation.CommandRunner:291)
ksqldb            | [2021-08-18 12:20:01,883] INFO Re
```

## Configuring your confluent connectors
These curl commands are taken from [script.sh](script.sh). Refer this file for more clarity.
#### Mqtt-kafka Connector

```bash
curl -s -X PUT -H  "Content-Type:application/json" http://localhost:8083/connectors/source-mqtt/config \
            -d '{
            "connector.class": "io.confluent.connect.mqtt.MqttSourceConnector",
            "tasks.max": "1",
            "mqtt.server.uri": "tcp://mosquitto:1883",
            "mqtt.topics":"truck_details_mqtt",
            "kafka.topic":"truck_details_kafka",
            "value.converter": "org.apache.kafka.connect.converters.ByteArrayConverter",
            "mqtt.qos": "2",
            "confluent.topic.bootstrap.servers": "kafka:29092",
            "confluent.topic.replication.factor": "1"
        }'
```
#### Kafka-ElasticSearch Connectors
```bash
curl -s -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
 "name": "elasticsearch-connector",
 "config": {
   "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
   "connection.url": "http://elasticsearch:9200",
   "tasks.max": "1",
   "topics": "truck_details_kafka",
   "type.name": "_doc",
   "value.converter": "org.apache.kafka.connect.json.JsonConverter",
   "value.converter.schemas.enable": "false",
   "schema.ignore": "true",
   "key.ignore": "true"
 }
}'
```
External References
- Connector => https://docs.confluent.io/kafka-connect-mqtt/current/mqtt-sink-connector/index.html
- KSQL => https://ksqldb.io/quickstart.html?_ga=2.147083639.1372971405.1629279822-621626216.1629279822
- MQTT to Kafka => https://github.com/SINTEF-9012/kafka-mqtt-source-connector
- https://docs.confluent.io/kafka-connect-mqtt/current/mqtt-source-connector/mqtt_source_connector_quickstart.html