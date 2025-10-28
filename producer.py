from kafka import KafkaProducer
import json, time, random, datetime

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

regions = ["Bogotá","Antioquia","Valle","Caribe","Central"]

try:
    while True:
        now = datetime.datetime.utcnow()
        record = {
            "fecha": now.strftime("%Y-%m-%d"),
            "hora": now.strftime("%H:%M:%S"),
            "region": random.choice(regions),
            "demanda_mwh": round(random.uniform(800,3200),2),
            "generacion_mwh": round(random.uniform(700,3300),2),
            "precio_cop_mwh": round(random.uniform(100000,300000),2),
            "fuente_generacion": random.choice(["hidro","termica","solar","eolica"])
        }
        producer.send("energia_consumo", record)
        print("Enviado:", record)
        time.sleep(2)
except KeyboardInterrupt:
    print("Producer detenido")
finally:
    producer.close()
