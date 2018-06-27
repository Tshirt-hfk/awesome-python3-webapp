# create database biblog
use biblog;

# table user
create table user(
id varchar(50) primary key,				#用户id
email varchar(50) unique,				#用户emial
name varchar(50) unique,				#用户名字
passwd varchar(50) not null,			#用户密码
image varchar(50) not null,				#用户图片url
signature varchar(100),					#用户简介
created_at double not null,				#创建时间
follower_number int not null default 0,	#粉丝数目
attentioner_number int not null default 0	#关注数目
);

# table blog
create table blog(
id varchar(50) primary key,				#博文id
user_id varchar(50) not null,			#用户id
blog_image varchar(50),					#博文图片
title varchar(50) not null,				#博文标题
intro varchar(250) not null,			#博文简介
content text not null,					#博文内容
created_at double not null				#创建时间
);

# table comment_of_blog		一级评论
create table comment_of_blog(
id varchar(50) primary key,				#评论id
blog_id varchar(50) not null,			#博文id
user_id varchar(50) not null,			#用户id
content text,							#评论内容
created_at double not null				#创建时间
);

#table comment_of_comment	二级评论
create table commment_of_blog(
id varchar(50) primary key,				#评论id
comment_id varchar(50) not null,		#一级评论id		
user_id varchar(50) not null,			#用户id
content text,							#评论内容
created_at double not null				#创建时间
);

# table favorite
create table favorite(
user_id varchar(50) not null,			#用户id
blog_id varchar(50) not null,			#博文id
created_at double not null,				#收藏时间
primary key PK_favorite(user_id, blog_id)
);

# table follower		粉丝
create table follower(
user_id varchar(50) not null,			#用户id
follower_id varchar(50) not null,		#粉丝id
created_at double not null,				#创建时间
primary key PK_fans(user_id, follower_id)
);

# table attentioner		关注
create table attentioner(
user_id varchar(50) not null,			#用户id
attentioner_id varchar(50) not null,	#关注人id
created_at double not null,				#关注时间
primary key PK_fans(user_id, attentioner_id)
);

#table dynamicstate
create table dynamicstate(
user_id varchar(50) not null,			#用户id
blog_id varchar(50) not null,			#博文id
created_at double not null,				#博文发布时间
primary key PK_dynamicstate(user_id, blog_id)
);
