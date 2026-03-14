-- Hospital Management System Database Setup
-- Run this script once to create the database and tables.

CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    age         INT NOT NULL,
    gender      ENUM('Male', 'Female', 'Other') NOT NULL,
    phone       VARCHAR(15),
    address     TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lab reports table
CREATE TABLE IF NOT EXISTS lab_reports (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    patient_id  INT NOT NULL,
    test_name   VARCHAR(100) NOT NULL,
    value       VARCHAR(50) NOT NULL,
    unit        VARCHAR(30),
    normal_range VARCHAR(50),
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);
