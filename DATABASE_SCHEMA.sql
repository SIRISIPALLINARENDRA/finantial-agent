-- Financial AI Agent Platform Database Schema
-- MySQL 8.0+

-- Database Creation
CREATE DATABASE IF NOT EXISTS financial_agent_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE financial_agent_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB;

-- Watchlist Table
CREATE TABLE IF NOT EXISTS watchlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(200),
    notes VARCHAR(500),
    alert_threshold JSON,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_ticker (ticker),
    UNIQUE KEY unique_user_ticker (user_id, ticker)
) ENGINE=InnoDB;

-- Query History Table
CREATE TABLE IF NOT EXISTS query_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    query_type VARCHAR(50) NOT NULL,
    query_params JSON,
    agent_response JSON,
    response_summary VARCHAR(1000),
    execution_time_ms INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_query_type (query_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;

-- Sample Data (Optional for testing)
-- INSERT INTO users (email, username, hashed_password, full_name, is_active)
-- VALUES
-- ('demo@example.com', 'demo_user', '$2b$12$...', 'Demo User', TRUE);

-- Performance Optimization Indexes
ALTER TABLE users ADD INDEX idx_active_users (is_active, created_at);
ALTER TABLE query_history ADD INDEX idx_user_created (user_id, created_at);
ALTER TABLE watchlists ADD INDEX idx_user_added (user_id, added_at);

-- Views for Analytics
CREATE OR REPLACE VIEW user_activity_summary AS
SELECT
    u.id,
    u.username,
    u.email,
    COUNT(DISTINCT w.id) as watchlist_count,
    COUNT(DISTINCT qh.id) as query_count,
    MAX(qh.created_at) as last_query_date
FROM users u
LEFT JOIN watchlists w ON u.id = w.user_id
LEFT JOIN query_history qh ON u.id = qh.user_id
GROUP BY u.id, u.username, u.email;

-- Query Performance Stats
CREATE OR REPLACE VIEW query_performance_stats AS
SELECT
    query_type,
    COUNT(*) as total_queries,
    AVG(execution_time_ms) as avg_execution_time_ms,
    MIN(execution_time_ms) as min_execution_time_ms,
    MAX(execution_time_ms) as max_execution_time_ms
FROM query_history
GROUP BY query_type;
