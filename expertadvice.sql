-- Create the users table first if it does not exist
CREATE TABLE IF NOT EXISTS users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- Create the expert_advice table
CREATE TABLE IF NOT EXISTS expertadvice (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,               -- Unique ID for each expert advice
    user_id INT(11) NOT NULL,                             -- Foreign key to the user requesting advice
    QUERY TEXT NOT NULL,                                  -- Query submitted by the user
    STATUS VARCHAR(50) NOT NULL DEFAULT 'pending',        -- Status of the request, default is 'pending'
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the advice was created
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Foreign key constraint with ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- The ON DELETE CASCADE option means that if a user is deleted from the users table, 
-- all related entries in the expert_advice table will be deleted automatically.
