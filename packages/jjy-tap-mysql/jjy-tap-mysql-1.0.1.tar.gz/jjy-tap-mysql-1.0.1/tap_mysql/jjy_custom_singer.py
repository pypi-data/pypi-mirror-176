from kafka import KafkaProducer
import json


def jjy_custom_singer_write_message(message, config=None, method=None):
    if method == "do_discover":
        to_kafka_msg = message
    else:
        to_kafka_msg = json.dumps(message.asdict(), use_decimal=True)
    print("配置信息: ", config)
    print("生产者消息: ", message)
    print("调用方法(默认为None): ", method)
    if config:
        kafka_ip = config.get("kafka_ip")
        kafka_port = config.get("kafka_port")
        kafka_topic = config.get("kafka_topic")
        producer = KafkaProducer(
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            bootstrap_servers=[f'{kafka_ip}:{kafka_port}']
        )
        producer.send(kafka_topic, to_kafka_msg)
        producer.close()
