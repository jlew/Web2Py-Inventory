# coding: utf8
# try something like
def index(): return dict(message="hello from manage.py")

def addItem():
    form = SQLFORM(db.item)
    
    if form.accepts(request.vars, session):
        response.flash = T("Item Added to Inventory")
    elif form.errors:
       response.flash = T("Form Has Errors, Item Not Added")
    return dict(form=form)
    
def checkIn():
    return dict(message="Coming Soon")
    
def checkOut():
    return dict(message="Coming Soon")
