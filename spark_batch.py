from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, hour, col, avg

spark = SparkSession.builder.appName("EnergiaBatch").getOrCreate()

# Leer CSV desde HDFS
df = spark.read.option("header","true").option("inferSchema","true").csv("hdfs:///data/energia/raw/energia_historica.csv")

# Normalizar y limpieza
df = df.withColumn("fecha", to_date(col("fecha"), "yyyy-MM-dd"))

# Asegurarnos de que 'hora' se pueda transformar en integer de hora
df = df.withColumn("hora_int", hour(col("hora")))

df_clean = df.na.drop(subset=["demanda_mwh","region","fecha","hora_int"])

# Agregado: demanda promedio por region y hora
res = df_clean.groupBy("region","hora_int").agg(avg("demanda_mwh").alias("demanda_promedio_mwh"))

# Mostrar y guardar
res.show(truncate=False)
res.write.mode("overwrite").parquet("hdfs:///data/energia/processed/demanda_por_region.parquet")

spark.stop()
