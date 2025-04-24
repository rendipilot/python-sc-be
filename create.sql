CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('admin', 'teacher', 'student');

-- Table: users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50),
    email VARCHAR,
    password VARCHAR(100),
    role user_role,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Table: teachers
CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Table: histories
CREATE TABLE histories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    user_id UUID REFERENCES users(id),
    creativity_score FLOAT NOT NULL,
    logical_score FLOAT NOT NULL,
    complexity_score FLOAT NOT NULL,
    level_score FLOAT NOT NULL,
    created_at TIMESTAMP
);
