-- sudo mysql < mysql_init.sql
-- mysql -u root -p < mysql_init.sql

-- change password rule
SET GLOBAL validate_password.policy=LOW;
SET GLOBAL validate_password.length=6;

-- create a workspace database
DROP DATABASE IF EXISTS EHAHC;
CREATE DATABASE EHAHC;

-- Create a user for the workspace database
CREATE USER 'ehahc'@'localhost' IDENTIFIED BY '114514';
GRANT ALL PRIVILEGES ON EHAHC.* TO 'ehahc'@'localhost';
FLUSH PRIVILEGES;

-- recovery password rule
SET GLOBAL validate_password.policy = MEDIUM;
SET GLOBAL validate_password.length = 8;

-- create tables
use EHAHC;

CREATE TABLE Student (
Curtin_ID INT PRIMARY KEY,
Password VARCHAR(255) NOT NULL,
Student_name VARCHAR(100) NOT NULL,
Student_email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Chat_history (
Chat_ID INT AUTO_INCREMENT PRIMARY KEY, 
Use_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
Student_input TEXT NOT NULL, 
Bot_answer TEXT NOT NULL, 
Curtin_ID INT, 
FOREIGN KEY (Curtin_ID) REFERENCES Student(Curtin_ID) ON DELETE CASCADE
);

CREATE TABLE Search_history (
Chat_ID INT AUTO_INCREMENT PRIMARY KEY, 
Use_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
Student_input TEXT NOT NULL, 
Bot_answer TEXT NOT NULL, 
Curtin_ID INT, 
FOREIGN KEY (Curtin_ID) REFERENCES Student(Curtin_ID) ON DELETE CASCADE
);