# -*- coding: utf-8 -*- 

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('Inventory Management')

#http://dev.w3.org/html5/markup/meta.name.html 
response.meta.author = 'Justin Lewis (jlew.blackout@gmail.com)'
response.meta.description = 'Inventory Management built on the Web2py framework'
response.meta.keywords = 'web2py, python, inventory management'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2010'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Home'), False, URL(request.application,'default','index'), []),
    (T('Browse'), False, "#", [
        (T('Inventory'), False, URL(request.application, 'browse', 'index'), []),
        (T('People'), False, URL(request.application, 'browse', 'people'), []),
    ] ),
    (T('Reports'), False, '#', [
        (T('All Inventory'), False, URL(request.application,'report','all'), []),
        (T('Checked Out Items'), False, URL(request.application,'report','checkedOut'), []),
        (T('Checked In Items'), False, URL(request.application,'report','checkedIn'), []),
        (T('Out by Person'), False, URL(request.application,'report','outByPerson'), []),
        (T('Items By...'), False, "#", [
            (T('Category'), False, URL(request.application,'report','itemsBy', args='Category'), []),
            (T('Condition'), False, URL(request.application,'report','itemsBy', args='CurrentCondition'), []),
            (T('Location'), False, URL(request.application,'report','itemsBy', args='HomeLocation'), []),
            (T('Status'), False, URL(request.application,'report','itemsBy', args="Status"), []),
        ]),
    ]),
    ]
if auth.has_membership("check_in") or auth.has_membership("check_out") or auth.has_membership("add_inventory"):
    mnu = []
    
    if auth.has_membership("add_inventory"):
        mnu.append((T('Add Inventory'), False, URL(request.application,'manage','addItem'), []))
    
    if auth.has_membership("check_in"):
        mnu.append((T('Check In'), False, URL(request.application,'manage','checkIn'), []))
        
    if auth.has_membership("check_out"):
        mnu.append((T('Check Out'), False, URL(request.application,'manage','checkOut'), []))
        
    response.menu.append((T('Manage Inventory'), False, "#", mnu))
    
if auth.has_membership("admin"):
    response.menu.append((T('Manage System Users'), False, URL(request.application,'plugin_useradmin','index'), []))
