# Live Maps

## Kafka Setup


1. Extract into kafka/ folder
2. Add `kafka/bin/windows` to environment variables
3. Create broker

   ```
   cd kafka/
   
   # Create UUID that will act as cluster ID (one time)
   kafka-storage.bat random-uuid
   
   # Format brokers and pass the cluster ID as -t (one time)
   # --standalone is used for single node KRaft cluster
   
   kafka-storage.bat format -t RqpVXZVATtSoF8T8u8vsBQ -c config\server.properties --standalone
   
   # Run Kafka broker
   kafka-server-start.bat config\server.properties
   
   ```

   \
   For multiple brokers, instead of `--standalone` each should have different `server.properties` mentioning a list of - `<node.id>@<host>:<controller_port>`

   \
   ```javascript
   controller.quorum.voters=1@localhost:9093,2@localhost:9094 
   ```

   \
4. Create a topic

   ```javascript
   # Create a topic
   kafka-topics.bat --bootstrap-server localhost:9092 --topic testBusData --create --partitions 1 --replication-factor 1
   ```

   `--replication-factor` = Controller automatically assigns the topic to these number of brokers

   `--partitions` = Number of partitions in that topic
5. Start a console producer to manually send messages to topic

   ```javascript
   kafka-console-producer.bat --bootstrap-server localhost:9092 --topic testBusData
   ```
6. Start a console consumer

   ```javascript
   kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic testBusData --from-beginning
   ```


```javascript
kafka-server-start.bat config\server.properties
python bd1.py
python app.py
```


