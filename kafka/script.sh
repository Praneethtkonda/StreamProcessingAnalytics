curl -s -X PUT -H  "Content-Type:application/json" http://localhost:8083/connectors/source-mqtt/config \
            -d '{
            "connector.class": "io.confluent.connect.mqtt.MqttSourceConnector",
            "tasks.max": "1",
            "mqtt.server.uri": "tcp://127.0.0.1:1883",
            "mqtt.topics":"spa_mqtt_topic",
            "kafka.topic":"ratings",
            "mqtt.qos": "2",
            "confluent.topic.bootstrap.servers": "kafka:29092",
            "confluent.topic.replication.factor": "1"
        }'
curl -s -X DELETE -H  "Content-Type:application/json" http://localhost:8083/connectors/source-mqtt/