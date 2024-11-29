
-- Create the database (if it doesn't already exist)
CREATE DATABASE IF NOT EXISTS chatbot_db;

-- Switch to the chatbot_db database
USE chatbot_db;

-- Create the bot_responses table
CREATE TABLE IF NOT EXISTS bot_responses (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,   -- Unique ID for each response
    question VARCHAR(255) NOT NULL,           -- User's query or key phrase
    response TEXT NOT NULL                    -- Bot's response to the query
);

-- Insert sample data into the bot_responses table
INSERT INTO bot_responses (question, response) VALUES
("what is organic farming", "Organic farming is a method of farming that avoids the use of synthetic fertilizers, pesticides, and herbicides."),
("how can i improve soil health", "You can improve soil health by using organic compost, rotating crops, and planting cover crops."),
("what is the best irrigation method for rice", "The best irrigation method for rice is flood irrigation, as it requires waterlogged fields."),
("what are the benefits of crop rotation", "Crop rotation helps improve soil fertility, reduces pest buildup, and prevents diseases."),
("tell me about pest control methods", "Integrated pest management (IPM) uses a combination of biological, cultural, mechanical, and chemical control methods to manage pests.");

-- Optionally, you can add more questions and responses as needed
-- Example:
-- INSERT INTO bot_responses (question, response) VALUES
-- ("what is hydroponics", "Hydroponics is a method of growing plants without soil, using mineral nutrient solutions in an aqueous solvent.");
