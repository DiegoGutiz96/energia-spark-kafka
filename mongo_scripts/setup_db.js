/*
  setup_db.js
  - Usa este script dentro de mongosh con: load("mongo_scripts/setup_db.js")
  - Crea colecciones y añade documentos base de clientes y equipos
*/

db = db.getSiblingDB("consumo_energia");

// Crear colecciones (si no existen)
db.createCollection("clientes");
db.createCollection("equipos_medicion");
db.createCollection("mediciones");

// Insertar clientes base
db.clientes.insertMany([
  { _id: "CL001", nombre: "Juan Pérez", direccion: "Medellín", tipo_cliente: "Residencial", estrato: 3 },
  { _id: "CL002", nombre: "María Gómez", direccion: "Bogotá", tipo_cliente: "Residencial", estrato: 4 },
  { _id: "CL003", nombre: "Carlos Ruiz", direccion: "Cali", tipo_cliente: "Comercial", estrato: 3 }
]);

// Insertar equipos base
db.equipos_medicion.insertMany([
  { _id: "MED1001", tipo_equipo: "Inteligente", fabricante: "Siemens", instalado_en: "CL001", fecha_instalacion: "2023-02-15" },
  { _id: "MED1002", tipo_equipo: "Inteligente", fabricante: "Landis", instalado_en: "CL002", fecha_instalacion: "2023-03-01" },
  { _id: "MED1003", tipo_equipo: "Analógico", fabricante: "ABB", instalado_en: "CL003", fecha_instalacion: "2023-01-20" }
]);
