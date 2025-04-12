CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Datos mínimos de prueba
INSERT INTO users (name, email) VALUES
('Juan Pérez', 'juan@example.com'),
('Ana Gómez', 'ana@example.com');
