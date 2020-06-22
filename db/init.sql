CREATE DATABASE variants;
use variants;

CREATE TABLE processed_data (
  chromosome VARCHAR(2),
  position INTEGER(20),
  id VARCHAR(20),
  changeFrom VARCHAR(50),
  changeTo VARCHAR(50),
  cancer VARCHAR(7)
);
