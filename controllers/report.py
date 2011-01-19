# coding: utf8
# try something like
def index(): return dict(message="hello from report.py")

def all():
    return dict(report=db(db.item.id>0).select())
    
def checkedOut():
    return dict(report=db(db.item.CheckedOut != None).select())

def checkedIn():
    return dict(report=db(db.item.CheckedOut == None).select())
    
def outByPerson():
    out = []
    for person in db(db.person.id > 0).select(orderby=db.person.Last_Name):
        items = db(db.item.CheckedOut == person).select()
        if items:
           out.append( (db.person._format % person, items) )
            
        
    return dict(res= out)

def itemsBy():
    out = {}
    for item in db(db.item.id > 0).select():
        the_key = item[request.args(0)]
        
        if not out.has_key(the_key):
            out[the_key] = [item]
        else:
            out[the_key] += [item]
    return dict(out=out)
