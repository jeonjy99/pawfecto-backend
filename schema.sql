
CREATE TABLE account_brand (
  brand_id INT NOT NULL AUTO_INCREMENT,
  login_id VARCHAR(30) NOT NULL UNIQUE,
  login_password VARCHAR(255) NOT NULL,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  phone_number VARCHAR(20),
  pet_type ENUM('dog', 'cat') NULL,
  style_profile TEXT,
  profile_image_url VARCHAR(255),
  PRIMARY KEY (brand_id)
);


CREATE TABLE account_creator (
  creator_id INT NOT NULL AUTO_INCREMENT,
  login_id VARCHAR(30) NOT NULL UNIQUE,
  login_password VARCHAR(255) NOT NULL,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  phone_number VARCHAR(20),
  address VARCHAR(255),
  pet_type ENUM('dog', 'cat') NULL,
  sns_handle VARCHAR(50),
  sns_url VARCHAR(255),
  total_post_count INT DEFAULT 0,
  follower_count INT DEFAULT 0,
  style_profile TEXT,
  profile_image_url VARCHAR(255),
  PRIMARY KEY (creator_id)
);

CREATE TABLE campaign (
  campaign_id INT NOT NULL AUTO_INCREMENT,
  brand_id INT NOT NULL,
  product_name VARCHAR(100),
  product_image_url VARCHAR(255),
  product_description TEXT,
  target_pet_type ENUM('dog', 'cat') NULL,
  min_follower_count INT DEFAULT 0,
  requested_at DATETIME,
  application_deadline_at DATE,
  posting_start_at DATE,
  posting_end_at DATE,
  required_creator_count INT,
  PRIMARY KEY (campaign_id),
  FOREIGN KEY (brand_id) REFERENCES account_brand(brand_id)
);


CREATE TABLE campaign_acceptance (
  campaign_acceptance_id INT NOT NULL AUTO_INCREMENT,
  creator_id INT NOT NULL,
  campaign_id INT NOT NULL,
  acceptance_status ENUM('pending', 'accepted', 'rejected', 'completed') DEFAULT 'pending',
  applied_at DATETIME,
  selected_at DATETIME,
  PRIMARY KEY (campaign_acceptance_id),
  FOREIGN KEY (creator_id) REFERENCES account_creator(creator_id),
  FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id)
);

CREATE TABLE deliverable (
  deliverable_id INT NOT NULL AUTO_INCREMENT,
  campaign_acceptance_id INT NOT NULL,
  posted_at DATETIME,
  post_url VARCHAR(255),
  deliverable_status ENUM('incomplete', 'completed') DEFAULT 'incomplete',
  PRIMARY KEY (deliverable_id),
  FOREIGN KEY (campaign_acceptance_id) REFERENCES campaign_acceptance(campaign_acceptance_id)
);
