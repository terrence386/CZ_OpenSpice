import tornado.web
from pycket.session import SessionMixin
from bokeh.embed import server_document
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('template'))

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self): #重写get_current_user()方法
        return self.session.get('username',None) #session是一种会话状态，跟数据库的session可能不一样
        
#添加装饰器,装饰需要验证的请求
class IndexHandler(AuthBaseHandler):
    
    @tornado.web.authenticated   #@tornado.web.authenticated装饰器包裹get方法时，表示这个方法只有在用户合法时才会调用，authenticated装饰器会调用get_current_user()方法获取current_user的值，若值为False，则重定向到登录url装饰器判断有没有登录，如果没有则跳转到配置的路由下去，但是要在app.py里面设置login_url
    def get(self,*args,**kwargs):
        user = self.get_current_user()  
        self.render('index.html',user=user)


class Spice_Xyce_Handler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        template = env.get_template('spice.html')
        script = server_document('http://localhost:5006/bkapp')
        self.write(template.render(script=script))

        # script = server_document('http://localhost:5006/bkapp')
        # self.render('spice.html',script=script)
