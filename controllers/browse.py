# coding: utf8
# try something like
def index():
    return dict(
        grid=plugin_jqgrid(db.item, height=400, 
                       columns=['id', 'BarCode', 'SerialNumber', 'Name', 'Category', 'HomeLocation', 'Status'],
                       onselect="document.location = 'http://%s%s/' + id;" % (request.env.http_host, URL("browse","item"))))
                       
def item():
    item = db(db.item.id==request.args(0)).select().first()
    if item:
        return dict(item=item)
    else:
        response.view = "error404.html"
        return dict(error_title = T("Item Not Found"), error_body=T("The requested item was not found in our inventory."))

@auth.requires_login()
def people():
    return dict(
        grid=plugin_jqgrid(db.person, height=400, col_width=150,
                       columns=['id', 'First_Name', 'Last_Name', 'Email'],
                       onselect="document.location = 'http://%s%s/' + id;" % (request.env.http_host, URL("browse","person"))))
                       
@auth.requires_login()
def person():
    person=db(db.person.id==request.args(0)).select().first()
    
    if person:
        return dict(person=person)
    else:
        response.view = "error404.html"
        return dict(error_title = T("Person Not Found"), error_body=T("The requested person was not found in our database."))
