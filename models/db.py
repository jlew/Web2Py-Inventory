# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

DATE_FORMAT = "%m/%d/%y %H:%M:%S %p"

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:0a715450-99df-4dc2-a70e-0bd3f458dd1d'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('person',
    Field('First_Name', 'string', length=40, required=True, label="First Name"),
    Field('Last_Name', 'string', length=40, required=True, label="Last Name"),
    Field('dce', 'string', required=True, label="DCE or Email"),
    Field('phone', 'string', length=20, label="Phone Number"),
    Field('search_name',compute=lambda r: "%s, %s (%s)" %( r['Last_Name'], r['First_Name'], r['dce'])),
    format="%(Last_Name)s, %(First_Name)s (%(dce)s)"
)

db.define_table('item',
    Field('Name'),
    Field('Description', 'text'),
    Field('Category'),
    Field('BarCode', unique=True),
    Field('HomeLocation'),
    Field('Value'),
    Field('Condition', label="Item Condition", default="New"),
    Field('Status', default="Avaliable"),
    Field('CreationDate', 'datetime', default=request.now, writable=False),
    Field('ModificationDate', 'datetime', default=request.now, update=request.now, writable=False),
    Field('CheckedOut', "reference person", requires=IS_EMPTY_OR(IS_IN_DB(db, db.person.id, db.person._format), null=None), readable=False, writable=False),
    Field('Comments', 'text'),
    format="%(Name)s: %(BarCode)s"
)

db.define_table('item_log',
    Field('Date', 'datetime', default=request.now, writable=False),
    Field('item', db.item),
    Field('msg')
)

db.item.Name.widget = SQLFORM.widgets.autocomplete(request,
                            db.item.Name, limitby=(0,40), min_length=0, orderby=db.item.Name)
db.item.Category.widget = SQLFORM.widgets.autocomplete(request,
                            db.item.Category, limitby=(0,40), min_length=0, orderby=db.item.Category)
db.item.HomeLocation.widget = SQLFORM.widgets.autocomplete(request,
                            db.item.HomeLocation, limitby=(0,40), min_length=0, orderby=db.item.HomeLocation)
db.item.Condition.widget = SQLFORM.widgets.autocomplete(request,
                            db.item.Condition, limitby=(0,40), min_length=0, orderby=db.item.Condition)
db.item.Status.widget = SQLFORM.widgets.autocomplete(request,
                            db.item.Status, limitby=(0,40), min_length=0, orderby=db.item.Status)
                            
db.item.CheckedOut.widget = SQLFORM.widgets.autocomplete(request, db.person.search_name,
                            id_field=db.person.id, limitby=(0,10), min_length=0, orderby=db.person.search_name)

#from gluon.contrib.populate import populate
#populate(db.person,50)
#populate(db.item,200)
#populate(db.item_log,500)
