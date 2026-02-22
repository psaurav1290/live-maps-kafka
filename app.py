from flask import Flask, render_template, Response
from confluent_kafka import Consumer, KafkaError

def get_kafka_consumer(topicname):
    conf = {
        'bootstrap.servers': '127.0.0.1:9092',
        'group.id': 'flask_consumer_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([topicname])
    return consumer

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/topic/<topicname>')
def get_messages(topicname):
    consumer = get_kafka_consumer(topicname)

    def events():
        try:
            while True:
                msg = consumer.poll(1.0)  # 1 second timeout
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        break
                yield f"data:{msg.value().decode('utf-8')}\n\n"
        finally:
            consumer.close()

    return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
