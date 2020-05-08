import cmd
import mysql.connector
import pandas as pd


class MysqlClient:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            database="socialnetwork",
            user="root",
            password="970610wjyWJY"
        )
        self.cursor = self.connection.cursor()

    def executeSqlQuery(self, query, vals=None):
        self.cursor.execute(query, vals)
        return self.cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()


class SocialNetworkClient(cmd.Cmd):
    intro = 'Welcome to Social Network Database.   Type help to list commands.\n'
    prompt = 'Social Network:  '

    def __init__(self):
        super(SocialNetworkClient, self).__init__()
        self.client = MysqlClient()
        self.current_user_id = None
        self.cursor = self.client.cursor
        self.returnFlag = False

    def check_if_login(self):
        if not self.current_user_id:
            print("Please login in first!")
            self.returnFlag = True
            return

    def do_signup(self,args):
        username = input("User Name: ")
        check_user_name_query = "SELECT userName FROM User WHERE userName = '{}';".format(username)
        check_user_name_result = self.client.executeSqlQuery(check_user_name_query).fetchall()
        if check_user_name_result:
            print("User Name has already been used. Please use another name")
            return
        signup_user_query = "insert into User (userName) values ('{}');".format(username)
        self.client.executeSqlQuery(signup_user_query)
        self.client.commit()

        print("User {} has been created.".format(username))

    def do_login(self,args):
        username = input("User Name: ")

        login_user_query = "SELECT * FROM User WHERE userName = '{}';".format(username)
        res = self.client.executeSqlQuery(login_user_query).fetchall()
        if not res:
            print("Error. User does not exist. Please re-enter user name.")
            return
        self.current_user_id = res[0][0]
        print("Welcome Back, {}!".format(username))

    def do_logout(self,args):
        print("You have been logged out!")
        self.current_user_id = None

    def do_post(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        description = input("Post title for this post: ")
        if not description:
            print("Please enter post title!")
            return
        topicName = input("Post topic for this post: ")
        if not topicName:
            print("Please enter topic name for post!")
            return
        try:
            if topicName and description:
                topicID = None
                post_topic_query = "SELECT topicID FROM Topic WHERE topicName = '{}';".format(topicName)
                res = self.client.executeSqlQuery(post_topic_query).fetchall()
                if res:
                    topicID = res[0][0]
                else:
                    create_topic_query = "INSERT INTO Topic (topicId,topicName) VALUES (%s,%s);"
                    vals = (topicID, topicName)
                    topicID = self.client.executeSqlQuery(create_topic_query, vals).lastrowid

                if topicID:
                    create_post_query = "INSERT INTO Post (userID, description) VALUES (%s, %s);"
                    vals = (self.current_user_id, description)
                    postID = self.client.executeSqlQuery(create_post_query, vals).lastrowid

                    if postID:
                        create_post_topic_query = "INSERT INTO Post_Topic VALUES (%s,%s);"
                        vals = (postID, topicID)
                        self.client.executeSqlQuery(create_post_topic_query, vals)
                        self.client.commit()
                        print("Post: {} has been created".format(description))
                
        except mysql.connector.Error as error:
            print("Error: Can not create post: {}".format(error))
            self.client.rollback()

    def do_show_latest_post(self,args):
        try:
            show_post_query = "SELECT * FROM Post ORDER BY postID DESC limit 10"
            post_record = self.client.executeSqlQuery(show_post_query).fetchall()
            for rec in post_record:
                print(rec[2])

        except mysql.connector.Error as error:
            print("Error: Can not show post: {}".format(error))
            self.client.rollback()

    def do_get_user_post(self, arg):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return
        userName = input("Enter the name of the user you want to see his/her post: ")
        if not userName:
            print("User name can not be empty")
            return
        try:
            get_user_id_query = "SELECT userID FROM User WHERE userName = '{}';".format(userName)
            userID = self.client.executeSqlQuery(get_user_id_query).fetchall()

            if not userID:
                print("User {} does not exist").format(userName)
                return
            userID = userID[0][0]
            get_user_post_query = "SELECT * FROM POST WHERE userID = {}".format(userID)
            res = self.client.executeSqlQuery(get_user_post_query).fetchall()

            user_post = pd.DataFrame(res, columns=[
                'postID',
                'userID',
                'description',
                'thumbUp',
                'thumbDown',
                'createTime',
            ])
            print(user_post)
        except mysql.connector.Error as error:
            print("Error: Can not show post: {}".format(error))
            self.client.rollback()

    def do_create_group(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        groupName = input("Group Name: ")
        groupType = input("Group Type: ")
        if not groupName or not groupType:
            print("Group Name or Group Type can not be empty")
            return
        try:
            create_group_query = "INSERT INTO Group_s (groupID, groupName, groupType) values (NuLL, '{}', '{}');".format(groupName, groupType)
            groupID = self.client.executeSqlQuery(create_group_query).lastrowid
            insert_user_group_query = "INSERT INTO User_Group (groupID, userID) values (%s, %s);"
            vals = (groupID, self.current_user_id)
            self.client.executeSqlQuery(insert_user_group_query, vals)
            print("Group: {} has been created".format(groupName))
            self.client.commit()
        except mysql.connector.Error as error:
            print("Error: Can not create group: {}".format(error))
            self.client.rollback()

    def do_join_group(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        groupName = input("The group name you want to join: ")
        if not groupName:
            print("Group Name can not be empty")
            return
        try:
            get_group_id_query = "SELECT groupID FROM Group_s WHERE groupName = '{}';".format(groupName)
            groupID = self.client.executeSqlQuery(get_group_id_query).fetchall()[0][0]
            if not groupID:
                print("Group does not exist")
                return
            check_user_group_query = "SELECT groupID,userID FROM User_Group WHERE groupID = '{}' AND userID = '{}';".format(groupID, self.current_user_id)
            check_user_group_result = self.client.executeSqlQuery(check_user_group_query).fetchall()
            if check_user_group_result:
                print("You have already joined this group!")
                return
            join_group_query = "INSERT INTO User_Group (groupID, userID) values (%s, %s);"
            vals = (groupID, self.current_user_id)
            self.client.executeSqlQuery(join_group_query, vals)
            self.client.commit()
            print("You have successfully join group {}".format(groupName))

        except mysql.connector.Error as error:
            print("Error: Can not join group: {}".format(error))
            self.client.rollback()

    def do_get_group_user(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        groupName = input("Enter the group name you want to check: ")
        if not groupName:
            print("Group name can not be empty")
            return
        try:
            get_group_id_query = "SELECT groupID FROM Group_s WHERE groupName = '{}';".format(groupName)
            groupID = self.client.executeSqlQuery(get_group_id_query).fetchall()
            if not groupID:
                print("Group: {} does not exist".format(groupName))
                return
            groupID = groupID[0][0]

            get_group_user_query = "SELECT groupName, userName FROM User WHERE userID IN (SELECT userID FROM User_Group WHERE groupID = {});".format(groupID)
            res = self.client.executeSqlQuery(get_group_user_query).fetchall()
            group_user = pd.DataFrame(res, columns=[
                'userName'
            ])
            print(group_user)

        except mysql.connector.Error as error:
            print("Error: Can not show group user: {}".format(error))
            self.client.rollback()

    def do_follow_user(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        follow_user_name = input("Enter the name of the user you want to follow: ")
        if not follow_user_name:
            print("User name can not be empty!")
            return
        try:
            get_follow_user_id_query = "SELECT userID FROM User WHERE userName = '{}';".format(follow_user_name)
            res = self.client.executeSqlQuery(get_follow_user_id_query).fetchall()
            if not res:
                print("User does not exist!")
                return
            follow_user_id = res[0][0]

            check_follow_user_query = "SELECT userID,followerID FROM Follower WHERE userID = {0} AND followerID = {1};".format(
                follow_user_id, self.current_user_id)
            check_follow_user_result = self.client.executeSqlQuery(check_follow_user_query).fetchall()
            if check_follow_user_result:
                print("You have already follow this user!")
                return
            else:
                follow_user_query = "INSERT INTO Follower (userID,followerID) VALUES (%s,%s);"
                vals = (follow_user_id, self.current_user_id)
                self.client.executeSqlQuery(follow_user_query, vals)
                self.client.commit()
                print("You have successfully follow {}".format(follow_user_name))

        except mysql.connector.Error as error:
            print("Error: Can not follow user: {}".format(error))
            self.client.rollback()

    def do_get_user_followers(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        userName = input("Enter the user name you want to check for follower: ")
        if not userName:
            print("User name can not be empty")
            return
        try:
            get_user_id_query = "SELECT userID FROM User WHERE userName = '{}';".format(userName)
            userID = self.client.executeSqlQuery(get_user_id_query).fetchall()
            if not userID:
                print("User: {} does not exist".format(userName))
                return
            userID = userID[0][0]

            get_follower_name_query = "SELECT userID, userName FROM User WHERE userID IN (SELECT followerID FROM Follower WHERE userID = {});".format(userID)
            res = self.client.executeSqlQuery(get_follower_name_query).fetchall()
            follower_name = pd.DataFrame(res, columns=[
                'userID',
                'userName'
            ])
            print(follower_name)

        except mysql.connector.Error as error:
            print("Error: Can not get followers: {}".format(error))
            self.client.rollback()



    def do_follow_topic(self,arg):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        follow_topic_name = input("Enter the topic name you want to follow: ")
        if not follow_topic_name:
            print("Topic name can not be empty!")
            return
        try:
            get_follow_topic_id_query = "SELECT topicID FROM Topic WHERE topicName = '{}';".format(follow_topic_name)
            res = self.client.executeSqlQuery(get_follow_topic_id_query).fetchall()
            if not res:
                print("Topic does not exist!")
                return
            follow_topic_id = res[0][0]

            check_follow_topic_query = "SELECT userID,topicID FROM User_Topic WHERE userID = {0} AND topicID = {1};".format(
                self.current_user_id, follow_topic_id)
            check_follow_topic_result = self.client.executeSqlQuery(check_follow_topic_query).fetchall()
            if check_follow_topic_result:
                print("You have already follow this topic!")
                return
            else:
                follow_topic_query = "INSERT INTO User_Topic (userID,topicID) VALUES (%s,%s);"
                vals = (self.current_user_id, follow_topic_id)
                self.client.executeSqlQuery(follow_topic_query, vals)
                self.client.commit()
                print("You have followed {}".format(follow_topic_name))

        except mysql.connector.Error as error:
            print("Error: Can not follow topic: {}".format(error))
            self.client.rollback()

    def do_thumbs_up(self,arg):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        thumbUpPostID = input("Enter the post ID you want to thumbs up: ")
        if not thumbUpPostID:
            print("Post ID can not be empty!")
            return
        try:
            get_post_name_query = "SELECT description FROM Post WHERE postID = {};".format(thumbUpPostID)
            postName = self.client.executeSqlQuery(get_post_name_query).fetchall()
            if not postName:
                print("Post does not exist")
                return
            postName = postName[0][0]
            update_thumbs_up_query = "UPDATE Post SET thumbUp = thumbUp + 1 WHERE postID = {};".format(thumbUpPostID)
            self.client.executeSqlQuery(update_thumbs_up_query)
            self.client.commit()
            print("You have thumbed up post: {}".format(postName))

        except mysql.connector.Error as error:
            print("Error: Can not thumb up: {}".format(error))
            self.client.rollback()

    def do_thumbs_down(self,arg):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        thumbDownPostID = input("Enter the post ID you want to thumbs down: ")
        if not thumbDownPostID:
            print("Post ID can not be empty!")
            return
        try:
            get_post_name_query = "SELECT description FROM Post WHERE postID = {};".format(thumbDownPostID)
            postName = self.client.executeSqlQuery(get_post_name_query).fetchall()
            if not postName:
                print("Post does not exist")
                return
            postName = postName[0][0]
            update_thumbs_down_query = "UPDATE Post SET thumbDown = thumbDown + 1 WHERE postID = {};".format(thumbDownPostID)
            self.client.executeSqlQuery(update_thumbs_down_query)
            self.client.commit()
            print("You have thumbed down post: {}".format(postName))

        except mysql.connector.Error as error:
            print("Error: Can not thumb down: {}".format(error))
            self.client.rollback()

    def do_comment_post(self,args):
        self.returnFlag = False
        self.check_if_login()
        if self.returnFlag:
            return

        postID = input("Enter the post ID you want to comment: ")
        comment = input("Leave your comment here: ")

        if not postID:
            print("Post ID can not be empty!")
            return
        if not comment:
            print("Comment can not be empty!")
            return

        try:
            get_post_query = "SELECT description FROM Post WHERE postID = {};".format(postID)
            res = self.client.executeSqlQuery(get_post_query).fetchall()

            if not res:
                print("Post does not exist! Please re enter postID.")
                return

            postName = res[0][0]
            commentID = None
            insert_comment_query = "INSERT INTO Post_Comment(commentID,postID,comment_content) VALUES (%s,%s,%s);"
            vals = (commentID, postID, comment)
            self.client.executeSqlQuery(insert_comment_query, vals)
            self.client.commit()
            print("You have comment on post: {}".format(postName))

        except mysql.connector.Error as error:
            print("Error: Can not comment on post: {}".format(error))
            self.client.rollback()



if __name__ == '__main__':
    SocialNetworkClient().cmdloop()

