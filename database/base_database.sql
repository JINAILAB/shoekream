CREATE TABLE shoes (
    id INT PRIMARY KEY,
    shoe_name VARCHAR(256) NOT NULL,
    shoe_category VARCHAR(64),
    original_price_with_currency INT,
    date_released DATE,
    colorway VARCHAR(64),
    gender VARCHAR(16),
    brand VARCHAR(32),
    wish_count INT DEFAULT 0,
    review_count INT DEFAULT 0,
    image_url_right VARCHAR(512),
    image_url_left VARCHAR(512),
    image_url_top VARCHAR(512),
    image_dir_right VARCHAR(512),
    image_dir_left VARCHAR(512),
    image_dir_top VARCHAR(512)
);

CREATE TABLE shoe_prices (
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    shoe_id INT,
    price INT,
    date_created DATETIME,
    FOREIGN KEY (shoe_id) REFERENCES shoes(id) ON DELETE CASCADE
);

CREATE TABLE style_image (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    shoe_id INT,
    image_url VARCHAR(512),
    FOREIGN KEY (shoe_id) REFERENCES shoes(id) ON DELETE CASCADE
)
