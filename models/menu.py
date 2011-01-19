# -*- coding: utf-8 -*- 

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html 
response.meta.author = 'you'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2010'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Home'), False, URL(request.application,'default','index'), []),
    (T('Manage Inventory'), False, URL(request.application,'manage','index'), [
        (T('Add Inventory'), False, URL(request.application,'manage','addItem'), []),
        (T('Check In'), False, URL(request.application,'manage','checkIn'), []),
        (T('Check Out'), False, URL(request.application,'manage','checkOut'), []),
    ]),
    (T('Reports'), False, '#', [
        (T('All Inventory'), False, URL(request.application,'report','all'), []),
        (T('Checked Out Items'), False, URL(request.application,'report','checkedOut'), []),
        (T('Checked In Items'), False, URL(request.application,'report','checkedIn'), []),
        (T('Out by Person'), False, URL(request.application,'report','outByPerson'), []),
        (T('Items By...'), False, "#", [
            (T('Category'), False, URL(request.application,'report','itemsBy', args='Category'), []),
            (T('Condition'), False, URL(request.application,'report','itemsBy', args='Condition'), []),
            (T('Location'), False, URL(request.application,'report','itemsBy', args='HomeLocation'), []),
            (T('Status'), False, URL(request.application,'report','itemsBy', args="Status"), []),
        ]),
    ]),
    ]

##########################################
## this is here to provide shortcuts
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################

#########################################
## Make your own menus
##########################################

response.menu+=[
    (T('This App'), False, URL('admin', 'default', 'design/%s' % request.application),
     [
            (T('Controller'), False, 
             URL('admin', 'default', 'edit/%s/controllers/%s.py' \
                     % (request.application,request.controller=='appadmin' and
                        'default' or request.controller))), 
            (T('View'), False, 
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))),
            (T('Layout'), False, 
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)),
            (T('Stylesheet'), False, 
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)),
            (T('DB Model'), False, 
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)),
            (T('Menu Model'), False, 
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)),
            (T('Database'), False, 
             URL(request.application, 'appadmin', 'index')),
                          
            (T('Errors'), False, 
             URL('admin', 'default', 'errors/%s' \
                     % request.application)), 
                     
            (T('About'), False, 
             URL('admin', 'default', 'about/%s' \
                     % request.application)), 
             
            ]
   )]
