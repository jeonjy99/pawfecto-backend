CREATE TABLE accounts_user (
  id INT NOT NULL AUTO_INCREMENT,                  
  password VARCHAR(50) NOT NULL,                  
  username VARCHAR(50) NOT NULL UNIQUE,           
  email VARCHAR(50) NOT NULL UNIQUE,

  -- Custom fields
  account_type ENUM('brand', 'creator') NOT NULL,
  name VARCHAR(50) NOT NULL,
  phone_number VARCHAR(20),

  pet_type ENUM('dog', 'cat') NULL,                            
  profile_image VARCHAR(255),
  profile_image_url VARCHAR(255),

  address TEXT,
  sns_handle VARCHAR(50),
  sns_url VARCHAR(255),
  total_post_count INT,
  follower_count INT,

  style_tags ENUM(
    'outdoor','energetic','no_preference','minimal',
    'aesthetic','heartfelt','cozy','wholesome','funny','calm'
  ),

  PRIMARY KEY (id)
);


CREATE TABLE campaign (
  campaign_id INT NOT NULL AUTO_INCREMENT,
  brand_id INT NOT NULL,                                

  product_name VARCHAR(100),
  product_image_url VARCHAR(255),
  product_description TEXT,

  pet_type ENUM('dog', 'cat'),
  min_follower_count INT DEFAULT 0,

  requested_at DATETIME NOT NULL,
  application_deadline_at DATE,

  style_tags ENUM(
    'outdoor','energetic','no_preference','minimal',
    'aesthetic','heartfelt','cozy','wholesome','funny','calm'
  ),

  posting_start_at DATE,
  posting_end_at DATE,

  required_creator_count INT,

  PRIMARY KEY (campaign_id),
  FOREIGN KEY (brand_id) REFERENCES accounts_user(id)
);


CREATE TABLE campaign_acceptance (
  campaign_acceptance_id INT NOT NULL AUTO_INCREMENT,

  creator_id INT NOT NULL,                     
  campaign_id INT NOT NULL,                    

  acceptance_status ENUM('pending','accepted','rejected','completed') DEFAULT 'pending',
  applied_at DATETIME,
  accepted_at DATETIME,

  PRIMARY KEY (campaign_acceptance_id),
  FOREIGN KEY (creator_id) REFERENCES accounts_user(id),
  FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id)
);


CREATE TABLE deliverable (
  deliverable_id INT NOT NULL AUTO_INCREMENT,

  campaign_acceptance_id INT NOT NULL,         

  posted_at DATETIME,
  post_url VARCHAR(255),
  deliverable_status ENUM('incomplete','completed') DEFAULT 'incomplete',

  PRIMARY KEY (deliverable_id),
  FOREIGN KEY (campaign_acceptance_id) REFERENCES campaign_acceptance(campaign_acceptance_id)
);


