from pyflink.common import SimpleStringSchema, Configuration
from pyflink.common.typeinfo import Types, RowTypeInfo
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic, CheckpointingMode, \
    ExternalizedCheckpointCleanup
from pyflink.datastream.connectors import DeliveryGuarantee
from pyflink.datastream.connectors.kafka import KafkaSource, \
    KafkaOffsetsInitializer, KafkaSink, KafkaRecordSerializationSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream.functions import MapFunction


def python_data_stream(producer_topic, consumer_topic):
    env = StreamExecutionEnvironment.get_execution_environment()
    # Set the parallelism to be one to make sure that all data including fired timer and normal data
    # are processed by the same worker and the collected result would be in order which is good for
    # assertion.
    env.set_parallelism(1)
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    # enabling and configuring checkpointing
    # https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/fault-tolerance/checkpointing/

    # start a checkpoint every 1000 ms
    env.enable_checkpointing(interval=1000)

    # advanced checkpointing options:
    # set mode to exactly-once (this is the default)
    env.get_checkpoint_config().set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
    # make sure 500 ms of progress happen between checkpoints
    env.get_checkpoint_config().set_min_pause_between_checkpoints(500)
    # checkpoints have to complete within one minute, or are discarded
    env.get_checkpoint_config().set_checkpoint_timeout(60000)
    # enable externalized checkpoints which are retained after job cancellation
    env.get_checkpoint_config().enable_externalized_checkpoints(ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION)

    # checkpoint storage
    configuration = Configuration()
    # configuration.set_string("state.backend.checkpoint-storage", "filesystem")
    checkpoints_local_dir = "file:///opt/pyflink/tmp/checkpoints/logs"
    configuration.set_string("state.checkpoints.dir", checkpoints_local_dir)
    env.configure(configuration)

    type_info: RowTypeInfo = Types.ROW_NAMED(['device_id', 'temperature', 'execution_time'],
                                             [Types.LONG(), Types.DOUBLE(), Types.INT()])

    json_row_schema = JsonRowDeserializationSchema.builder().type_info(type_info).build()

    # source -- our consumer data
    source = KafkaSource.builder() \
        .set_bootstrap_servers('kafka:9092') \
        .set_topics(producer_topic) \
        .set_group_id('pyflink-e2e-source') \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(json_row_schema) \
        .build()

    # to send processed data to another topic
    # this topic should be already created
    sink = KafkaSink.builder() \
        .set_bootstrap_servers('kafka:9092') \
        .set_record_serializer(KafkaRecordSerializationSchema.builder()
                               .set_topic(consumer_topic)
                               .set_value_serialization_schema(SimpleStringSchema())
                               .build()
                               ) \
        .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
        .build()

    # getting a datastream from the source
    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")

    # data transformation
    # convert Kelvins -> Celsius
    ds.map(TemperatureFunction(), Types.STRING()) \
        .sink_to(sink)
    env.execute_async("Devices preprocessing with local checkpoints")


class TemperatureFunction(MapFunction):

    def map(self, value):
        device_id, temperature, execution_time = value
        return str({"device_id": device_id, "temperature": temperature - 273, "execution_time": execution_time})


if __name__ == '__main__':
    producer_topic = "checkpoints-local-topic"
    consumer_topic = "checkpoints-local-topic-processed"
    python_data_stream(producer_topic, consumer_topic)
