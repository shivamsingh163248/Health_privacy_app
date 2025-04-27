CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    email VARCHAR(100),
    blood_group VARCHAR(10),
    mobile VARCHAR(15),
    city VARCHAR(100),
    zip_code VARCHAR(10),
    state VARCHAR(100),
    donation_date DATE
);
