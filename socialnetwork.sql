DROP DATABASE IF EXISTS socialnetwork;
CREATE DATABASE socialnetwork;
USE socialnetwork;

SET NAMES utf8mb4;

CREATE TABLE Vocation (
	vocationID		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    vocationType    varchar(100)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Gender (
	genderID		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    genderType		VARCHAR(100)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Relationship (
	relationshipID	 INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    relationshipType VARCHAR(100)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE User (
	userID			INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    vocationID		INT,
    genderID		INT,
    relationshipID	INT,
    userName		VARCHAR(100),
    birthDate 		DATE,
    address 		VARCHAR(100),
    bio				VARCHAR(500),
    email			VARCHAR(100),
    FOREIGN KEY (vocationID) REFERENCES Vocation(vocationID) ON DELETE CASCADE,
    FOREIGN KEY (genderID) REFERENCES Gender(genderID) ON DELETE CASCADE,
	FOREIGN KEY (relationshipID) REFERENCES Relationship(relationshipID) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Group_s (
	groupID		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    groupName	VARCHAR(100),
    groupType   VARCHAR(100)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE User_Group (
	groupID		INT NOT NULL ,
    userID		INT NOT NULL ,
    PRIMARY KEY (groupID, userID),
	FOREIGN KEY (groupID) REFERENCES Group_s(groupID) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Follower (
	userID		INT NOT NULL,	  
    followerID	INT NOT NULL,
    PRIMARY KEY (userID, followerID),
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (followerID) REFERENCES User(userID) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Topic (
	topicID		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	topicName 	VARCHAR(100)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE User_Topic (
	userID		INT NOT NULL,
    topicID 	INT NOT NULL,
    PRIMARY KEY (userID, topicID),
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (topicID) REFERENCES Topic(topicID) ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Sub_Topic (
	topicID		INT NOT NULL,
    subtopicID 	INT NOT NULL,
    PRIMARY KEY (topicID, subtopicID),
    FOREIGN KEY (topicID) REFERENCES Topic (topicID) ON DELETE CASCADE,
    FOREIGN KEY (subTopicID) REFERENCES Topic (topicID) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Post (
	postID		   INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userID		   INT NOT NULL,
    description    VARCHAR(500),
    thumbUp        INT DEFAULT 0,
    thumbDown      INT DEFAULT 0,
    createTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Post_Link (
	postID			INT PRIMARY KEY NOT NULL,
    postLink		VARCHAR(100),
    FOREIGN KEY (postID) REFERENCES Post(postID) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- CREATE TABLE User_Post (
-- 	userID		INT,
--     postID		INT,
--     PRIMARY KEY (userID, postID),
--     FOREIGN KEY (postID) REFERENCES Post(postID) ON DELETE CASCADE,
--     FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE

-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- CREATE TABLE Comment (
-- 	commentID	INT PRIMARY KEY,
-- 	comment 	VARCHAR(500)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Post_Comment (
	commentID		INT NOT NULL AUTO_INCREMENT,
    postID			INT NOT NULL,
    comment_content	VARCHAR(500),
    PRIMARY KEY (commentID),
    FOREIGN KEY (postID) REFERENCES Post(postID) ON DELETE CASCADE
    -- FOREIGN KEY (commentID) REFERENCES Comment(commentID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Post_Topic(
	postID		INT NOT NULL,
    topicID		INT NOT NULL,
    PRIMARY KEY (postID, topicID),
    FOREIGN KEY (postID) REFERENCES Post(postID) ON DELETE CASCADE,
    FOREIGN KEY (topicID) REFERENCES Topic(topicID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

BEGIN;
INSERT INTO Vocation (vocationID,vocationType) VALUES 
	(1, 'Religious Life'), 
	(2, 'Priesthood'), 
	(3, 'Marriage'), 
	(4, 'Single Life'), 
	(5, 'Other');
COMMIT;

BEGIN;
INSERT INTO Gender (genderID,genderType) VALUES 
	(1, 'Female'), 
	(2, 'Male'), 
	(3, 'Other');
COMMIT;

BEGIN;
INSERT INTO Relationship (relationshipID,relationshipType) VALUES 
	(1, 'Single'), 
	(2, 'In a relationship'), 
	(3, 'Engaged'), 
	(4, 'Married'), 
	(5, 'In a civil union'), 
	(6, 'In a domestic partnership'), 
	(7, 'In an open relationship'), 
	(8, 'Divorced'), 
	(9, 'Widowed');
COMMIT;

BEGIN;
INSERT INTO User (userID,vocationID,genderID,relationshipID,userName,birthDate,address,bio,email) VALUES
	(1, 2, 3, 1, 'Bertram007', '1995-01-01', '256 Phillips St','I am Bertram, I love ECE', 'bertram007@gmail.com'),
    (2, 3, 2, 4, 'Austin666', '1996-12-31', '268 Lester St', 'I am Austin, I hate ECE', 'Austin666@yahoo.com'),
    (3, 4, 1, 1, 'Christine001', '1997-07-12', '250 University Ave', 'I like ECE 356 lol', 'christine001@gmail.com'),
    (4, 5, 2, 2, 'Edwardxxx', '1998-02-03', '130 University Ave W', 'I hate programming lol', 'edwardxxx@outlook.com'),
    (5, 3, 1, 4, 'Chole123', '1999-08-29', '8000 Yonge St', 'I love Waterloo!', 'chole123@uwaterloo.ca');
COMMIT;

BEGIN;
INSERT INTO Group_s (groupID, groupName, groupType) VALUES
	(1, 'Cowboy Bebop', 'Study'),
    (2, 'Star War', 'Movie'),
    (3, 'Dota', 'Game');
COMMIT;

BEGIN;
INSERT INTO User_Group (groupID, userID) VALUES
	(1,1),
    (1,2),
    (2,1),
    (2,3),
    (2,4),
    (3,5),
    (3,2);
COMMIT;

BEGIN;
INSERT INTO Follower (userID, followerID) VALUES
	(1,2),
    (1,3),
    (2,1),
    (2,4),
    (3,2),
    (3,4),
    (3,5),
    (4,2),
    (4,5),
    (5,1),
    (5,3);
COMMIT;

BEGIN;
INSERT INTO Topic (topicID, topicName) VALUES
	(1,'COVID-19'),(2,'sports'),(3,'entertainment'),(4,'finance'),
    (5,'COVID-19 US'),(6,'COVID-19 CANADA'),
    (7,'NBA'),(8,'NHL'),
    (9,'Billboard Top 100'),
    (10,'Nasdaq'),(11,'Dow Jones');
COMMIT;

BEGIN;
INSERT INTO Sub_Topic (topicID, subtopicID) VALUES
    (1,5),(1,6),
    (2,7),(2,8),
    (3,9),
    (4,10),(4,11);
COMMIT;

BEGIN;
INSERT INTO User_Topic (userID, topicID) VALUES
	(1,3),(1,7),(1,11),
    (2,4),(2,6),(2,8),
    (3,2),(3,5),(3,9),
    (4,4),(4,7),(4,10),
    (5,1),(5,5),(5,6);
COMMIT;


BEGIN;
INSERT INTO Post (postID, userID, description, thumbUp, thumbDown, createTime) VALUES
	(1,1,'How can we fulfill our academic admission?',57,3, "2020-03-20 20:32:17"),
    (2,2,'I like ECE, but ECE dont like me',15,1, "2020-04-01 15:37:29"),
    (3,4,'What to do in quarantine?',7,0,"2020-04-22 01:34:03"),
    (4,5,'Failed work term report, what should I do?',58,10,"2020-01-15 12:13:53"),
    (5,3,'How useful is a car for coop?',23,1,"2020-04-22 18:43:11");
COMMIT;


BEGIN;
INSERT INTO Post_Link (postID, postLink) VALUES
		(1,'www.socialnetwork.com/post1'),
		(2,'www.socialnetwork.com/post2'),
        (3,'www.socialnetwork.com/post3'),
        (4,'www.socialnetwork.com/post14'),
        (5,'www.socialnetwork.com/post5');
COMMIT;


BEGIN;
INSERT INTO Post_Topic (postID, topicID) VALUES
	(1,1),(1,3),(1,5),
    (2,3),(2,10),(2,11),
    (3,6),(3,7),(3,8),
    (4,2),(4,5),(4,9),
    (5,3),(5,4),(5,7),(5,10);
COMMIT;

INSERT INTO Post_Comment (postID, commentID, comment_content) VALUES
		(1,1, 'lmaoooooo'),
        (1,2, 'LOL'),
        (2,3, 'what???'),
        (2,4, 'I second this'),
        (3,5, 'I am not crying, there is just something in my eye'),
        (4,6, 'Damn, you are good!'),
        (5,7, 'I feel you');
COMMIT;

		