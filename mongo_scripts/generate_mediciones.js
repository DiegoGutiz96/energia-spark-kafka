/*
  generate_mediciones.js
  - Ejecutar desde mongosh con: load("mongo_scripts/generate_mediciones.js")
  - Genera 150 documentos únicos en consumo_energia.mediciones
*/

db = db.getSiblingDB("consumo_energia");

// Primero borramos mediciones si quieres empezar limpio (descomenta la siguiente línea si deseas reiniciar)
// db.mediciones.drop();

const medidores = ["MED1001", "MED1002", "MED1003", "MED1004", "MED1005", "MED1006", "MED1007", "MED1008"];

let docs = [];
for (let i = 1; i <= 150; i++) {
  // ID único por documento
  const id = `MED-${String(i).padStart(4, "0")}`;

  // Elegir medidor aleatorio (si el medidor no existe en equipos_medicion no importa)
  let medidor = medidores[Math.floor(Math.random() * medidores.length)];

  // Fecha aleatoria en enero 2024
  let dia = Math.floor(Math.random() * 28) + 1;
  let hora = Math.floor(Math.random() * 24);
  let fecha = new Date(Date.UTC(2024, 0, dia, hora, 0, 0)); // UTC para ISODate en mongosh

  docs.push({
    _id: id,
    medidor_id: medidor,
    fecha_hora: fecha,
    consumo_kwh: Number((Math.random() * (20 - 5) + 5).toFixed(2)), // entre 5 y 20 kWh
    estado: "OK"
  });
}

// Insertar en lotes por si son muchos
while (docs.length) {
  const batch = docs.splice(0, 50);
  db.mediciones.insertMany(batch);
}

print("Inserción finalizada. Documentos insertados:", db.mediciones.countDocuments());
