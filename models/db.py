# -*- coding: utf-8 -*- 

DATE_FORMAT = "%m/%d/%y %H:%M:%S %p"

#########################################################################
## Google App Engine Support
#########################################################################
if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB

import os
from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()


#########################################################################
## Private Auth settings should be read for private_cfg.ini if exists
#########################################################################
private_cfg = os.path.join(request.folder,"models","private_cfg.ini")
if os.path.exists( private_cfg ):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read(private_cfg)
    mail.settings.server = config.get('Mail', 'server')
    mail.settings.tls = config.get('Mail', 'tls')
    mail.settings.sender = config.get('Mail', 'sender')
    mail.settings.login = config.get('Mail', 'login')
    
    auth.settings.hmac_key = config.get('Auth', 'hmac_key')
    
else:
    mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
    mail.settings.sender = 'you@gmail.com'         # your email
    mail.settings.login = 'username:password'      # your credentials or None

    auth.settings.hmac_key = 'sha512:0a715450-99df-4dc2-a70e-0bd3f458dd1d'   # before define_tables()

auth.settings.create_user_groups = False
auth.settings.actions_disabled.append('register') 

auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'


crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Tables
#########################################################################

db.define_table('person',
    Field('First_Name', 'string', length=40, required=True, label=T("First Name")),
    Field('Last_Name', 'string', length=40, required=True, label=T("Last Name")),
    Field('Email', 'string', required=True, label=T("Email")),
    Field('Phone', 'string', length=20, label=T("Phone Number")),
    Field('search_name',compute=lambda r: "%s, %s (%s)" %( r['Last_Name'], r['First_Name'], r['Email'])),
    format="%(Last_Name)s, %(First_Name)s (%(Email)s)"
)

db.define_table('item',
    Field('Name', 'string', length=100, label=T("Name")),
    Field('Description', 'text', label=T("Description")),
    Field('Category', 'string', length=100, label=T("Category")),
    Field('BarCode', unique=True, label=T("Bar Code")),
    Field('SerialNumber', label=T("Serial Number")),
    Field('HomeLocation', 'string', label=T("Location")),
    Field('Value', label=T("Value")),
    Field('Condition', 'string', label=T("Condition"), default=T("New")),
    Field('Status', 'string', label=T("Status"), default=T("Avaliable")),
    Field('CreationDate', 'datetime', label=T("Creation Date"), default=request.now, writable=False),
    Field('ModificationDate', 'datetime', label=T("Last Modified"), default=request.now, update=request.now, writable=False),
    Field('CheckedOut', "reference person", label=T("Loaned To"), requires=IS_EMPTY_OR(IS_IN_DB(db, db.person.id, db.person._format), null=None), readable=False, writable=False),
    Field('Comments', 'text'),
    Field('Due', 'date', label=T("Return By"), comment=T("Optional due date"), requires=IS_EMPTY_OR(IS_DATE())),
    format="%(Name)s: %(BarCode)s"
)

db.define_table('item_log',
    Field('Date', 'datetime', default=request.now, writable=False),
    Field('item', db.item),
    Field('msg')
)

#########################################################################
## Auto Complete Widgets
#########################################################################
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


#########################################################################
## Setup Auth Groups
#########################################################################

if db(db.auth_group.role=="admin").count() == 0:
    auth.add_group(role = 'admin')
    auth.add_group(role = 'add_inventory')
    auth.add_group(role = 'check_in')
    auth.add_group(role = 'check_out')
    auth.add_group(role = 'edit_inventory')
