from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, DoubleType

schema = StructType() \
    .add("fecha", StringType()) \
    .add("hora", StringType()) \
    .add("region", StringType()) \
    .add("demanda_mwh", DoubleType()) \
    .add("generacion_mwh", DoubleType()) \
    .add("precio_cop_mwh", DoubleType()) \
    .add("fuente_generacion", StringType())

spark = SparkSession.builder.appName("EnergiaStreaming").getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers","localhost:9092") \
    .option("subscribe","energia_consumo") \
    .option("startingOffsets","latest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json")
parsed = json_df.select(from_json(col("json"), schema).alias("data")).select("data.*")

# Agregado de ejemplo: promedio en ventana de 1 minuto por region
agg = parsed.groupBy(window(col("hora"), "1 minute"), col("region")) \
            .avg("demanda_mwh") \
            .withColumnRenamed("avg(demanda_mwh)","demanda_promedio_mwh")

query = agg.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate","false") \
    .start()

query.awaitTermination()
