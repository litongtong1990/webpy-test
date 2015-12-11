# coding: UTF-8
import os
  
import sae
import web
import model
import push
from weixinInterface import WeixinInterface
from sae.storage import Bucket

urls = (
'/', 'Hello',
'/weixin','WeixinInterface',
'/ck','feedback',
'/upload','Upload',
'/book','Book',
)
  
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
  
class Hello:
    def GET(self):

    	domain_name = "ohnojack"          
    	s = sae.storage.Client()          
        path="kindle/"
        
        #bookname="让我去那花花世界.epub"
        bookname="身边的江湖.mobi"
        #bookname="2dfsd.txt"
        bookpath=(path+bookname).decode('utf-8')
        ob = s.get(domain_name, bookpath)
        data=ob.data
        push.push_kindle(data,bookname)
        
        return render.hello("helloxxx smsmsmsm");
     
class feedback:
    def GET(self):
        fkcon = model.get_fkcontent()
        return render.checkfk(fkcon)
    
class Upload:
    def GET(self):
        domain_name = "ohnojack"          
        s = sae.storage.Client()          
           
        bucket=Bucket('ohnojack')
        
        
        path="kindle/"
        bookname="身边的江湖.mobi"
        bookpath=(path+bookname).decode('utf-8')
        ob = s.get(domain_name, bookpath)        
        
        
        return render.Upload()
        #return bucket.list()
    
class Book:
    def GET(self):    
        domain_name = "ohnojack"   
        bucket=Bucket('%s'%domain_name)        
        return render.BookPage(bucket.list())        
           
    
     
app = web.application(urls, globals()).wsgifunc()
         
application = sae.create_wsgi_app(app)