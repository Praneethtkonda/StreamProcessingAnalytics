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
curl -s -X DELETE -H  "Content-Type:application/json" http://localhost:8083/connectors/source-mqtt/


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

curl -s -X DELETE -H  "Content-Type:application/json" http://localhost:8083/connectors/elasticsearch-connector/