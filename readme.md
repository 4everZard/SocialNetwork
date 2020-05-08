# Social Network


This project is used to simulate a simple social network system. It uses Mysql as database storage and has a CLI client with a set of well-defined APIs for clients.

## Getting Started
### Prerequisites
-'MySql8.0'

-'Python3.7'


### File Usage
1. socialnetwork.sql is our sql file to create database
2. main.py in the set of API file
3. ER Diagram.pdf is used to explain the ER Model for this project

### How to Run
1. Run socialnetwork.sql to create demo database on your own SQL server
2. Run following commands: 
    
    pip3 install pandas 
    
    pip3 install mysql-connector-python
    
    if you already have the above libs, skip it
3. Run main.py using python3 main.py
4. Enter api name after do_ in the CLI, you can also use 'help' to see what APIs are available


## API Documentation
- `check-if-login` 
    - Check if a user has logined, user should login first before performing any operations
    
- `sign up`
    - Sign up a user by taking CLI input as **username**
    - If a username has bee used in the system, username can not be created. That is to say, this database does not allow duplicate username

- `login`
    - Log in a user by takingCLI input as **username**
    - If username does not exist, CLI will return error message
 
- `logout`
    - Logout current user
    
- `post`
    - Make a post by taking **description** and **topicName** as input under current user
    - Description and topicName can not be empty
    - If topicName does not exist, create new topic in Topic table for topicName
    - If a user has succeeded making a post, a new entry will be inserted for User_Post table to link postID and userID


- `show_latest_post`
    - display most recent 10 posts with their titles
    
- `get_user_post`
    - Get all posts information under a specific user by taking **userName** as input
    - Input userName can not be empty
    - If user does not exist, CLI will return error message
    
- `create_group`
    - Create group by taking **groupName** and **groupType** as input
    - groupName and groupType can not be empty
    
- `join_group`
    - Join a group by taking groupName as input for current user
    - groupName can not be empty
    - If groupName does not exist, CLI will return error
    - A user can not join a group if already joined that group
    - If a user has succeeded joining a group, a new entry will be inserted for User_Group table to link userID and groupID
    
- `get_group_user`
    - Get all usernames for a specific group by taking **groupName** as input
    - groupName can not be empty
    - If this group does not exist, CLI will return error

- `follow_user`
    - Follow a specific user by taking **userName** as input
    - userName can not be empty
    - If this user does not exist, CLI will return error
    - A user can not follow another user if he/she has already follow that user

- `get_user_followers`
    - Get all the followers' usernames for a specific user by taking **userName** as input
    - User name can not be empty
    - If user does not exist, CLI will return error
    
- `follow_topic`
    - Follow a specific topic by taking **topicName** as input
    - topicName can not be empty
    - If this topic does not exist, CLI will return error
    - A user can not follow a topic if he/she has already follow that topic
    
- `thumbs_up`
    - Thumbs up for a specific post by taking **postID** as input
    - postID can not be empty
    - If post does not exist, CLI will return error
    - If post exists, the thumpUp value in Post table will increment by 1 for that post
    
- `thumbs_down`
    - Thumbs down for a specific post by taking **postID** as input
    - postID can not be empty
    - If post does not exist, CLI will return error
    - If post exists, the thumpDown value in Post table will decrement by 1 for that post
    
- `comment_post`
    - Comment a specific post by taking **postID** and **comment** as input
    - postID and comment can not be empty
    - If post dost not exist, it will return to CLI and let you re-enter another postID
    - If a user has successfully commented on a post, a new entry will be inserted to Post_Comment table to link commentID and postID
    
## Authors
    Jiayu Wu
