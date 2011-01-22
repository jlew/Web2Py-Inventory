# coding: utf8
# try something like
def index():
    redirect(URL('default','index'))

@auth.requires_membership("add_inventory")
def addItem():
    form = SQLFORM(db.item)
    
    if form.accepts(request.vars, session):
        response.flash = T("Item Added to Inventory")
    elif form.errors:
       response.flash = T("Form Has Errors, Item Not Added")
    return dict(form=form)
   
@auth.requires_membership("check_in") 
def checkIn():
    if request.vars.barcode:
        item = db(db.item.BarCode == request.vars.barcode).select().first()
        if item:
            if item.CheckedOut:
                if request.vars.msg:
                    comments = T("%s \n\n Checkin (%s) Comments: %s") % \
                                (item.Comments, item.CheckedOut['search_name'], request.vars.msg)
                else:
                    comments = item.Comments

                db.item_log.insert(item=item.id, msg=T("Checked In from %s") % item.CheckedOut['search_name'])
                item.update_record(CheckedOut=None, Comments=comments)
                response.flash = T("Item Checked In")
            else:
                response.flash = T("Error: Item not checked out")
                
        else:
            response.flash = T("Item Not Found")
    return dict()


@auth.requires_membership("check_out") 
def checkOut():
    add_user = SQLFORM(db.person)
    
    if add_user.accepts(request.vars, session):
        response.flash = T("Person added to System")
    elif add_user.errors:
       response.flash = T("Form has errors")
       
    if request.vars.person and request.vars.barcode:
        person = db(db.person.search_name == request.vars.person).select().first()
        item = db(db.item.BarCode == request.vars.barcode).select().first()
        
        if person and item:
            if not item.CheckedOut:
                if request.vars.msg:
                    comments = T("%s \n\n Checkin (%s) Comments: %s") % \
                                (item.Comments, person.search_name, request.vars.msg)
                else:
                    comments = item.Comments
                item.update_record(CheckedOut = person.id, Comments = comments)
                db.item_log.insert(item=item.id, msg=T("Checked out to %s") % person.search_name)
                response.flash = T("Item Checked Out")
            else:
                response.flash = T("Error, Item currently checked out In")
        else:
            response.flash = T("Person or Item not found")
    return dict(add_user=add_user)
    
def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    people = db(db.person.search_name.like('%'+partialstr+'%')).select(db.person.search_name)
    items = []
    for (i,person) in enumerate(people):
        items.append(DIV(A(person.search_name, _id="res%s"%i, _href="#", _onclick="copyToBox($('#res%s').html())"%i), _id="resultLiveSearch"))

    return TAG[''](*items)
