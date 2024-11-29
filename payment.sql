CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    payment_gateway_id VARCHAR(255), -- For storing Stripe's Session ID or PayPal Transaction ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);