# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const
import re 
from sae.storage import Bucket



db = web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST,
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB
)
  
def addfk(username, fktime, fkcontent):
    return db.insert('fk', user=username, time=fktime, fk_content=fkcontent)






def Add_Dating():
    return db.insert('Dating',Week=1,Quota_total=2)

def get_Quata_total():
    return db.select('Dating',order='Dating_Id')

def update_Quata_total(Dating_Id,Quota_total):
    return db.update('Dating', where='Dating_Id =  %s'%(Dating_Id), Quota_total = Quota_total)





  
def get_fkcontent():
    return db.select('fk', order='id')


def query_email(username):
    return db.select('fk', where='user =  "%s"'%username)    


def update_email(username,email):
    db.update('fk', where='user =  "%s"'%username, fk_content = email)

    
    
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0


def bookExist(bookname):
    domain_name = "ohnojack"   
    bucket=Bucket('%s'%domain_name)        
    booklist=[]
    bookExist=[]
    for item in bucket.list():
        booklist.append(item.name)
    for item in booklist:
        if bookname in item:
            bookExist.append(item)
    return bookExist
        
    