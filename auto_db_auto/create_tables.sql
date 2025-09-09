
CREATE TABLE IF NOT EXISTS games (
  game_id_rawg INT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  release_date DATE NULL,
  genres TEXT NULL,
  rating DECIMAL(4,2) NULL,
  metacritic INT NULL,
  updated_at_utc DATETIME NULL,
  last_ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS platforms (
  platform_id INT PRIMARY KEY,
  platform_name VARCHAR(100) NOT NULL,
  UNIQUE KEY uq_platform_name (platform_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS game_platforms (
  game_id_rawg INT NOT NULL,
  platform_id INT NOT NULL,
  PRIMARY KEY (game_id_rawg, platform_id),
  CONSTRAINT fk_gp_game FOREIGN KEY (game_id_rawg) REFERENCES games(game_id_rawg) ON DELETE CASCADE,
  CONSTRAINT fk_gp_platform FOREIGN KEY (platform_id) REFERENCES platforms(platform_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS api_state (
  state_key VARCHAR(64) PRIMARY KEY,
  state_value VARCHAR(255) NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS price_history (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  game_id_rawg INT NOT NULL,
  platform VARCHAR(32) NOT NULL DEFAULT 'PC',
  price DECIMAL(10,2) NOT NULL,
  shop VARCHAR(128) NULL,
  url TEXT NULL,
  ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_ph_game_ts (game_id_rawg, ts),
  CONSTRAINT fk_ph_game FOREIGN KEY (game_id_rawg) REFERENCES games(game_id_rawg) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS best_price_latest (
  game_id_rawg INT PRIMARY KEY,
  platform VARCHAR(32) NOT NULL DEFAULT 'PC',
  price DECIMAL(10,2) NULL,
  shop VARCHAR(128) NULL,
  url TEXT NULL,
  ts TIMESTAMP NULL,
  CONSTRAINT fk_bpl_game FOREIGN KEY (game_id_rawg) REFERENCES games(game_id_rawg) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
