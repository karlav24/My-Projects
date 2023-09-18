CREATE DATABASE IF NOT EXISTS photoshare;
USE photoshare;
DROP TABLE IF EXISTS Pictures CASCADE;
DROP TABLE IF EXISTS Users CASCADE;


CREATE TABLE Users (
    user_id int4 NOT NULL AUTO_INCREMENT,
    gender varchar(6),
    email varchar(255) NOT NULL UNIQUE,
    password varchar(40) NOT NULL,
    dob DATE DEFAULT '1970-01-01' NOT NULL,
    hometown varchar(40),
    fname varchar(40) NOT NULL,
    lname varchar(40) NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);
CREATE TABLE Albums(
  album_id int4 NOT NULL AUTO_INCREMENT,
  aname varchar(40) NOT NULL,
  date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
  user_id int4 NOT NULL,
  PRIMARY KEY (album_id),
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
CREATE TABLE Pictures
(
  picture_id int4  AUTO_INCREMENT,
  user_id int4,
  imgdata longblob ,
  caption VARCHAR(255),
  album_id int4 NOT NULL,
  INDEX upid_idx (user_id),
  CONSTRAINT pictures_pk PRIMARY KEY (picture_id),
  FOREIGN KEY(user_id) REFERENCES Users(user_id),
  FOREIGN KEY(album_id) REFERENCES Albums(album_id) ON DELETE CASCADE
);
CREATE TABLE Comments(
comment_id int4 NOT NULL AUTO_INCREMENT,
comment_text TEXT NOT NULL,
comment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
user_id int4,
picture_id int4 NOT NULL,
PRIMARY KEY(comment_id),
FOREIGN KEY(user_id) REFERENCES Users(user_id),
FOREIGN KEY(picture_id) REFERENCES Pictures(picture_id) ON DELETE CASCADE
);

CREATE TABLE Likes( 
  user_id int4 NOT NULL, 
  picture_id int4 NOT NULL, 
  PRIMARY KEY (picture_id, user_id), 
  FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE, 
  FOREIGN KEY (picture_id) REFERENCES Pictures (picture_id) ON DELETE CASCADE 
); 
 CREATE TABLE Tags(
	tag_id int4 AUTO_INCREMENT,
    name varchar(100),
    PRIMARY KEY(tag_id)
 );
 CREATE TABLE Tagged(
	picture_id int4,
    tag_id int4,
    PRIMARY KEY(picture_id, tag_id),
    FOREIGN KEY(picture_id) REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES Tags(tag_id)
 );
CREATE TABLE Friendship ( 
  UID1 int4 NOT NULL, 
  UID2 int4 NOT NULL, 
  CHECK (UID1 <> UID2), 
  PRIMARY KEY(UID1, UID2), 
  FOREIGN KEY (UID1) REFERENCES Users (user_id) ON DELETE CASCADE, FOREIGN KEY (UID2) REFERENCES Users (user_id) ON DELETE CASCADE );
  /*CREATE ASSERTION Comment-Constraint CHECK 
(NOT EXISTS (SELECT * FROM Comments C, Pictures P 
WHERE C.picture_id = P.picture_id AND P.user_id = C.user_id)*/

INSERT INTO Users (user_id, gender, email, password, dob, hometown, fname, lname) VALUES (0,'f', 'test@bu.edu', 'test','1990-01-01', 'neverland', 'chloe', 'v');
INSERT INTO Users (user_id, gender, email, password, dob, hometown, fname, lname) VALUES (0,'m', 'test2@bu.edu', 'test','1990-01-01', 'neverland', 'karla', 'v');
INSERT INTO Friendship(UID1, UID2) VALUES (1,2);
INSERT INTO Friendship(UID1, UID2) VALUES (2,1);

/*INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');
joe*/
