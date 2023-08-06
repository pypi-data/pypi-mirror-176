from kafka import KafkaProducer
import json
def jjy_custom_singer_write_message(message, config=None, method=None):
    # print(11111111111111111)
    print("在这进行的输出-------------------------------")
    if method == "do_discover":
        to_kafka_msg = message
    else:
        to_kafka_msg = json.dumps(message.asdict(), use_decimal=True)
    print(to_kafka_msg)
    print(config)
    # sys.stdout.write(format_message(message) + '\n')
    # sys.stdout.flush()
    print("在这进行的输出--结束-------------------------------")
    if config:
        # print("*******************   messages文件   *************************************")
        kafka_ip = config.get("kafka_ip")
        kafka_port = config.get("kafka_port")
        kafka_topic = config.get("kafka_topic")
        producer = KafkaProducer(
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            bootstrap_servers=[f'{kafka_ip}:{kafka_port}']
        )
        producer.send(kafka_topic, to_kafka_msg)
        producer.close()