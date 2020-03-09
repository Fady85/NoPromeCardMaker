import pymysql.cursors

class user():
    def __init__(self, database, username, password,host,port,socket):
        self.database=database
        self.username=username
        self.password=password
        self.port=port
        self.socket=socket
        self.host=host
    ####
    def addUser(self, mail, username, password):
        ## check if user exist return user ID else, add in db and return ID
        conn= pymysql.connect(
                host=self.host,  
                user=self.username, 
                password=self.password, 
                db=self.database,
                port=self.port,
                unix_socket=self.socket,
                charset="utf8")
        cur = conn.cursor()
        cur.execute("SELECT * FROM `user` WHERE `mail` = %s", (mail))
        user = cur.fetchone()
        if not user:
            cur.execute("""INSERT INTO `user`
                    (`mail`,`username`, `password`) 
                    VALUES (%s, %s, %s)""",(mail, username, password))
            conn.commit()
            cur.execute("SELECT LAST_INSERT_ID()")
            user = cur.fetchone()
            cur.execute("SELECT * FROM `user` WHERE `id` = %s", (user[0]))
            user = cur.fetchone()
        else:   
            return False
        cur.close() 
        conn.close()    
    ####
    def getUser(self, id=None, mail=None, username=None):
        conn= pymysql.connect(
                host=self.host,  
                user=self.username, 
                password=self.password, 
                db=self.database,
                port=self.port,
                unix_socket=self.socket,
                charset="utf8")
        cur = conn.cursor()
        if id: 
            cur.execute("SELECT * FROM `user` WHERE `id` = %s", (id))
            user = cur.fetchall()
        elif mail:
            cur.execute("SELECT * FROM `user` WHERE `mail` = %s", (mail))
            user = cur.fetchall()
        elif username:
            cur.execute("SELECT * FROM `user` WHERE `username` = %s", (username))
            user = cur.fetchall()
        cur.close() 
        conn.close()
        if user:
            return user
        else:
            return None
    ####    
    def login(self, password, mail=None, username=None):
        if mail:
            conn= pymysql.connect(
                host=self.host,  
                user=self.username, 
                password=self.password, 
                db=self.database,
                port=self.port,
                unix_socket=self.socket,
                charset="utf8")
            cur = conn.cursor()
            cur.execute("SELECT * FROM `user` WHERE `mail` = %s AND `password` = %s", (mail,password))
            user = cur.fetchone()
            cur.close() 
            conn.close()
            return user
        elif username:
            conn= pymysql.connect(
                host=self.host,  
                user=self.username, 
                password=self.password, 
                db=self.database,
                port=self.port,
                unix_socket=self.socket,
                charset="utf8")
            cur = conn.cursor()
            cur.execute("SELECT * FROM `user` WHERE `username` = %s AND `password` = %s", (username,password))
            user = cur.fetchone()
            cur.close() 
            conn.close()
            return user
        return None
    ####