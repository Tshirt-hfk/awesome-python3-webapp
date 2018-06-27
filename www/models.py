import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
	__table__ = 'user'
    
	id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')
	email = StringField(column_type='varchar(50)')
	passwd = StringField(column_type='varchar(50)')
	admin = BooleanField()
	name = StringField(column_type='varchar(50)')
	image = StringField(column_type='varchar(500)')
	created_at = FloatField(default=time.time)

class Blog(Model):
    __table__ = 'blog'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')
    user_id = StringField(column_type='varchar(50)')
    user_name = StringField(column_type='varchar(50)')
    user_image = StringField(column_type='varchar(500)')
    name = StringField(column_type='varchar(50)')
    summary = StringField(column_type='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Comment(Model):
    __table__ = 'comment'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')
    blog_id = StringField(column_type='varchar(50)')
    user_id = StringField(column_type='varchar(50)')
    user_name = StringField(column_type='varchar(50)')
    user_image = StringField(column_type='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)
"""


class User(Model):
	__table__ = 'user'
    
	id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')  #pk
	email = StringField(column_type='varchar(50)')                                  #unique
    name = StringField(column_type='varchar(50)')                                   #unique
	passwd = StringField(column_type='varchar(50)')
	image = StringField(column_type='varchar(50)')                                  #图片路径
    signature = StringField(column_type='varchar(100)')
	created_at = FloatField(default=time.time)                                      #创建时间
    follower_number = IntegerField()                                                #粉丝数目
    attentioner_number = IntegerField()                                             #关注数目

class Blog(Model):                  #博客
    __table__ = 'blog'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')  #pk
    user_id = StringField(column_type='varchar(50)')                                #foreign key 
    blog_image = StringField(column_type='varchar(50)')                             #图片路径
    title = StringField(column_type='varchar(50)')
    intro = StringField(column_type='varchar(250)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Comment_of_Blog(Model):       #一级评论
    __table__ = 'comment_of_blog'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')  #pk
    blog_id = StringField(column_type='varchar(50)')                                #foreign key 
    user_id = StringField(column_type='varchar(50)')                                #foreign key     
    content = TextField()
    created_at = FloatField(default=time.time)

class Comment_of_Comment(Model):    #二级评论
    __table__ = 'comment_of_comment'

    id = StringField(primary_key=True, default=next_id, column_type='varchar(50)')  #pk
    comment_id = StringField(column_type='varchar(50)')                             #foreign key 
    user_id = StringField(column_type='varchar(50)')                                #foreign key         
    content = TextField()
    created_at = FloatField(default=time.time)

class Favorite(Model):              #收藏夹
    __table__ = 'favorite'

    user_id = StringField(column_type='varchar(50)')
    blog_id = StringField(column_type='varchar(50)')
    created_at = FloatField(default=time.time)

class Follower(Model):              #粉丝
    __table__ = 'follower'

    user_id = StringField(column_type='varchar(50)')
    follower_id = StringField(column_type='varchar(50)')
    created_at = FloatField(default=time.time)

class Attentioner(Model):           #关注
    __table__ = 'attentioner'

    user_id = StringField(column_type='varchar(50)')
    attentioner_id = StringField(column_type='varchar(50)')
    created_at = FloatField(default=time.time)

class DynamicState(Model):          #动态
    __table__ = 'dynamicstate'

    user_id = StringField(column_type='varchar(50)')
    blog_id = StringField(column_type='varchar(50)')
    created_at = FloatField(default=time.time)
"""	
