CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    device_mac VARCHAR(255) NULL,
    credits INT NOT NULL DEFAULT 1000,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY ux_device_mac (device_mac)
);
CREATE TABLE ai_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT NOT NULL,
    html_content LONGTEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Migration note: If you already have an existing `users` table, run the following
-- SQL to add the `device_mac` column and unique index safely:
-- ALTER TABLE users
--   ADD COLUMN device_mac VARCHAR(255) NULL,
--   ADD UNIQUE INDEX ux_device_mac (device_mac);

-- To add the `credits` column for existing databases and set default starting credits to 1000,
-- run the following SQL (this will backfill existing rows with 1000 credits):
-- ALTER TABLE users
--   ADD COLUMN credits INT NOT NULL DEFAULT 1000;

-- Alternatively, run the provided Python migration script at
-- `scripts\add_device_mac_migration.py` which will add the column only if
-- it does not already exist.
