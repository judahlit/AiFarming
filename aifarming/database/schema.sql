CREATE TABLE IF NOT EXISTS cow (
  id VARCHAR(50) PRIMARY KEY,
  country VARCHAR(4),
  coat_color VARCHAR(50),
  hb_1 INTEGER,
  hb_2 INTEGER,
  hb_3 INTEGER,
  hb_4 INTEGER,

  birth_date VARCHAR,
  slaughter_date VARCHAR,
  lifetime_days INTEGER,
  slaughter_weight FLOAT
);

