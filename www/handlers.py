import time, re, asyncio, hashlib, logging, json
from coreweb import get, post
from aiohttp import web
from models import User, Blog, Comment
from apis import APIValueError, APIError
from models import next_id
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

def user2cookie(user, max_age):
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

#用户注册，并返回Cookie
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    d = dict()
    d['email']=email
    users = await User.findAll(**d)
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='about:blank')
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    r.content_type = 'text/plain;charset=utf-8'
    r.body = 'register:success'.encode('utf-8')
    return r

#用户登陆，并放回Cookie
@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    d = dict()
    d['email']=email
    users = await User.findAll(**d)
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('password', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    r.content_type = 'text/plain;charset=utf-8'
    r.body = 'signin:success'.encode('utf-8')
    return r

#主页
@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'index.html',
        'blogs': blogs,
		'__user__': request.__user__
    }

#注册页面
@get('/register')
def register():
	return {
		'__template__' : 'register.html'
	}

#登陆页面
@get('/signin')
def signin():
	return {
		'__template__' : 'signin.html'
	}

#用户登出
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

#admin的博文管理页面	
@get('/manage/blogs')
async def manage_blogs(request):
	return {
        '__template__': 'manage_blogs.html',
		'__user__': request.__user__
    }

#获取博文接口
@get('/api/blogs')
async def api_blogs(request):
	d = dict()
	d['user_id']=request.__user__.id
	blogs = await Blog.findAll(**d)
	if len(blogs) == 0:
		return None
	return {
        'blogs': blogs,
    }

#博文创建页面
@get('/manage/blogs/create')
def blog_create(request):
	return {
		'__template__': 'manage_blog_edit.html',
		'__user__': request.__user__
	}

#博文创建接口
@post('/api/create_blog')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog

#博文删除接口
@post('/api/delete_blog')
async def delete_blog(request, *, id):
    blog = await Blog.find(id)
    if not blog:
        raise APIValueError('blog', 'blog is not existed')
    await blog.remove()
    return "success"

#博文页面
@post('/api/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    if not blog:
        raise APIValueError('blog', 'blog is not existed')
    d = dict()
    d['blog_id'] = id
    comment = await Comment.findAll(**d)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comment': comment
    }


