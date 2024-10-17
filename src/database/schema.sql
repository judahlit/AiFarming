CREATE TABLE IF NOT EXISTS cow (
  id VARCHAR(50) PRIMARY KEY,
  sex VARCHAR(1),
  country VARCHAR(4),
  coat_color VARCHAR(50),

  birth_date DATE,
  slaughter_date DATE,
  lifetime_days INTEGER,
  slaughter_weight FLOAT
);

