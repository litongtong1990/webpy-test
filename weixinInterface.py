# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
import model
import sae
import push
import datetime
from lxml import etree
from sae.storage import Bucket


 
class WeixinInterface:
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="zyy" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        
 
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr



    def POST(self):
            str_xml = web.data() #获得post来的数据
            xml = etree.fromstring(str_xml)#进行XML解析
            content=xml.find("Content").text#获得用户所输入的内容
            msgType=xml.find("MsgType").text
            fromUser=xml.find("FromUserName").text
            toUser=xml.find("ToUserName").text
            
            today=datetime.datetime.now()
            #yesterday = today - datetime.timedelta(days=1)             

            dayOfWeek=today.weekday()

            if dayOfWeek==0:
                WhichDay=u"周一"
            elif dayOfWeek==1:
                WhichDay=u"周二"                
            elif dayOfWeek==2:
                WhichDay=u"周三"     
            elif dayOfWeek==3:
                WhichDay=u"周四"     
            elif dayOfWeek==4:
                WhichDay=u"周五"     
            elif dayOfWeek==5:
                WhichDay=u"周六"     
            else:
                WhichDay=u"周日"     

            user_list= ["you","me"]
            if fromUser not in user_list:           
                #return self.render.reply_text(fromUser,toUser,int(time.time()),u"闲杂人等退散~这个额度系统不对你们开放！！！")      
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"本周是%s！！！"%(WhichDay))      
            
            elif content == u"额度查询":
                results=model.get_Quata_total()
                result_this_week=results[0] 
                Quota_total=result_this_week.Quota_total
                if fromUser == user_list[0]:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u"富婆好，你本周的余额还有%s天"%(str(Quota_total)))
                else:
                    #model.Add_Dating()
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u"主人好，富婆的余额还有%s天"%(str(Quota_total)))            

            elif content.startswith("+") or content.startswith("-") :
                if fromUser == user_list[0]:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u"富婆好，你木有权限改变额度哦，把你男人伺候开心了没准他就帮你增加一天额度呢！")
                elif len(content)>1:
                    if content[1:].isdigit():
                        results=model.get_Quata_total()
                        result_this_week=results[0]
                        Dating_Id=result_this_week.Dating_Id   
                        Quota_total=result_this_week.Quota_total
                        if content.startswith("+"):
                            Quota_total+=int(content[1:])
                            model.update_Quata_total(Dating_Id,Quota_total)  
                            return self.render.reply_text(fromUser,toUser,int(time.time()),u"主人好，额度增加成功，富婆本周的额度是%s天"%(str(Quota_total)))            
                        else:
                            Quota_total-=int(content[1:])
                            model.update_Quata_total(Dating_Id,Quota_total)  
                            return self.render.reply_text(fromUser,toUser,int(time.time()),u"主人好，额度减少成功，本周的额度是%s天"%(str(Quota_total)))            
                        
                    else:
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u"%s不是有效输入，请输入+1 +2 等等"%(content))             
                else:
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u"%s不是有效输入，请输入+1 +2 等等"%(content))   
            else:
                return self.render.reply_text(fromUser,toUser,int(time.time()),time.strftime('%Y-%m-%d %H:%M',time.localtime()))
      
    # def POST(self):        
    #         str_xml = web.data() #获得post来的数据
    #         xml = etree.fromstring(str_xml)#进行XML解析
    #         content=xml.find("Content").text#获得用户所输入的内容
    #         msgType=xml.find("MsgType").text
    #         fromUser=xml.find("FromUserName").text
    #         toUser=xml.find("ToUserName").text
    #         bucket = Bucket('ohnojack')



    #         if msgType == 'text':
    #             content=xml.find("Content").text
    #             username=fromUser
    #             results=model.query_email(username)



    #             #绑定邮箱操作
    #             if content.startswith(u"绑定 "):       
    #                 emailAddress=content[3:]
    #                 if(model.validateEmail(emailAddress)==1):
    #                 	fktime = time.strftime('%Y-%m-%d %H:%M',time.localtime())   
                    	
    #                     #新用户绑定，增加一条记录
    #                     if len(results)==0:
    #                         model.addfk(fromUser,fktime,emailAddress.encode('utf-8'))         
    #                         return self.render.reply_text(fromUser,toUser,int(time.time()),u'您的邮箱'+emailAddress+u'已经绑定成功，如果想要更换绑定邮箱，再次发送【绑定 您的邮箱】进行邮箱绑定。')                    	
                        
                                                
    #                     #老用户更改绑定，改表中的邮箱地址
    #                     else:
    #                         item=results[0] 
    #                         OldEmailAddress=item.fk_content
    #                         model.update_email(username,emailAddress.encode('utf-8'))
   
    #                         return self.render.reply_text(fromUser,toUser,int(time.time()),u'您重新绑定邮箱'+emailAddress+u'成功')               
    #                 else:
    #                     return self.render.reply_text(fromUser,toUser,int(time.time()),u'请输入正确的邮箱格式，发送【绑定 您的邮箱】进行邮箱绑定')                
                
           
                
                
    #             booklist=model.bookExist(content)
                
    #             #假如已经绑定过邮箱，并且查询的书籍存在，则发送
    #             if (len(results)!=0 and len(booklist)!=0):
    #                 item=results[0] 
    #                 email=item.fk_content                    
    #                 domain_name = "ohnojack"          
    #                 s = sae.storage.Client()          

    #                 bookpath=booklist[0]
    #                 bookname=bookpath[7:]
    #                 sendwordsuccess= bookname+u"已经成功推送到您的kindle。"
    #                 sendwordfail= bookname+u"推送失败"                    
    #                 ob = s.get(domain_name, bookpath)
    #                 data=ob.data
    #                 pushresult=push.push_kindle(data,bookname,email)    
                    
    #                 if pushresult==1:
    #                     return self.render.reply_text(fromUser,toUser,int(time.time()),sendwordsuccess)                  
    #                 else:
    #                     return self.render.reply_text(fromUser,toUser,int(time.time()),sendwordfail)                           
    #             #假如已经绑定过邮箱，并且查询的书籍不存在，重新输入书名                
    #             elif (len(results)!=0 and (len(booklist)==0)):
    #                 return self.render.reply_text(fromUser,toUser,int(time.time()),u'您寻找的书籍不存在啊哈哈 这是测试svn的，请重新输入')                  
                
    #             #没有绑定过邮箱，则进行绑定
    #             else:
    #                 return self.render.reply_text(fromUser,toUser,int(time.time()),u'您第一次使用该公众号，请发送【绑定 您的邮箱】进行邮箱绑定')
                    
                
             
                
                
                