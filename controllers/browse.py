# coding: utf8
# try something like
def index():
    return dict(
        grid=plugin_jqgrid(db.item, height=400, 
                       columns=['id', 'BarCode', 'Name', 'Category', 'HomeLocation', 'Status'],
                       onselect="document.location = 'http://%s%s/' + id;" % (request.env.http_host, URL("browse","item"))))
                       
def item():
    return dict(item=db(db.item.id==request.args(0)).select().first())

def people():
    return dict(
        grid=plugin_jqgrid(db.person, height=400, col_width=150,
                       columns=['id', 'First_Name', 'Last_Name', 'dce'],
                       onselect="document.location = 'http://%s%s/' + id;" % (request.env.http_host, URL("browse","person"))))
def person():
    return dict(person=db(db.person.id==request.args(0)).select().first())
