DROP DATABASE IF EXISTS MyDatabase;
CREATE DATABASE MyDatabase;
USE MyDatabase;

-- Core Table: AuthenticationFactor (No Cost)
CREATE TABLE AuthenticationFactor (
    AuthFactorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Accuracy INT CHECK (Accuracy BETWEEN 1 AND 10),
    Intrusiveness INT CHECK (Intrusiveness BETWEEN 1 AND 10),
    Privacy INT CHECK (Privacy BETWEEN 1 AND 10),
    Effort INT CHECK (Effort BETWEEN 1 AND 10)
);

-- Insert Your 13 Authentication Methods
INSERT INTO AuthenticationFactor (Name, Accuracy, Intrusiveness, Privacy, Effort) VALUES
('Network Usage Pattern', 7, 1, 8, 1),
('Geo-Location', 7, 2, 8, 2),
('Device Fingerprinting', 8, 2, 6, 2),
('FIDO2 Security Key', 10, 3, 6, 3),
('Behavioral Biometrics', 7, 3, 7, 3),
('On-Device Prompt', 9, 4, 6, 4),
('Fingerprint', 8, 4, 6, 4),
('PIN', 6, 4, 8, 4),
('Face Recognition', 9, 5, 5, 5),
('Iris Scan', 9, 6, 6, 6),
('Voice Recognition', 8, 5, 5, 5),
('Password', 5, 6, 7, 6),
('Password + SMS', 8, 7, 6, 7);

-- Composite Ranking Query
SELECT 
    Name,
    Accuracy,
    Intrusiveness,
    Privacy,
    Effort,
    (0.4 * Accuracy) + 
    (0.3 * (10 - Intrusiveness)) +
    (0.2 * Privacy) +
    (0.1 * (10 - Effort)) AS CompositeScore
FROM AuthenticationFactor
ORDER BY CompositeScore DESC;
