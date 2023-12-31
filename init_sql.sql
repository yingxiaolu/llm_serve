USE `chat`;

DROP TABLE IF EXISTS lama;
CREATE TABLE lama (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  chat_id VARCHAR(1000) DEFAULT '',
  role VARCHAR(100) DEFAULT '',
  content TEXT,
  token INTEGER DEFAULT 0,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);