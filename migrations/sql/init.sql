--liquibase formatted sql

--changeset dev:1
CREATE TABLE IF NOT EXISTS operators (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    max_leads INTEGER NOT NULL DEFAULT 10,
    created_at DATETIME NOT NULL
);

--changeset dev:2
CREATE TABLE IF NOT EXISTS leads (
    id CHAR(36) PRIMARY KEY,
    external_id VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    email VARCHAR(255),
    name VARCHAR(255),
    created_at DATETIME NOT NULL
);

--changeset dev:3
CREATE TABLE IF NOT EXISTS sources (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL
);

--changeset dev:4
CREATE TABLE IF NOT EXISTS operator_weights (
    id CHAR(36) PRIMARY KEY,
    operator_id CHAR(36) NOT NULL,
    source_id CHAR(36) NOT NULL,
    weight INTEGER NOT NULL,
    FOREIGN KEY (operator_id) REFERENCES operators(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

--changeset dev:5
CREATE TABLE IF NOT EXISTS requests (
    id CHAR(36) PRIMARY KEY,
    lead_id CHAR(36) NOT NULL,
    source_id CHAR(36) NOT NULL,
    operator_id CHAR(36),
    message TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (source_id) REFERENCES sources(id),
    FOREIGN KEY (operator_id) REFERENCES operators(id)
);

--changeset dev:6
CREATE INDEX IF NOT EXISTS idx_requests_operator_active ON requests(operator_id, is_active);

--changeset dev:7
CREATE INDEX IF NOT EXISTS idx_requests_lead ON requests(lead_id);

--changeset dev:8
CREATE INDEX IF NOT EXISTS idx_operator_weights_source ON operator_weights(source_id);
