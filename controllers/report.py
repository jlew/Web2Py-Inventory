# coding: utf8
# try something like
def index():
    redirect(URL('default','index'))

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

        # Allow an item to be filtered (useful for rss)
        if request.vars.filter and the_key != request.vars.filter:
            continue

        if not out.has_key(the_key):
            out[the_key] = [item]
        else:
            out[the_key] += [item]

    # If rss, pad data
    if request.extension == "rss":
        entries = []
        for key,lst in out.items():
            checkedout = 0
            desc = ""
            for x in lst:
                if x.CheckedOut:
                    checkedout+=1

                desc += itemToTableRow(x).xml()

            entry = dict(
                    title=T("%(category)s: %(out)d of %(total)d on Loan") % {
                            "category": key,
                            "out": checkedout,
                            "total": len(out[key])
                        },
                    link="http://%s%s" % \
                            (request.env.http_host, 
                            URL('report','itemsBy', args=request.args(0), vars={'filter': key}, extension="")
                            ),
                    description=itemTableHeader().xml() + desc + "</table>"
                )
            entries.append(entry)

        return dict(
                    title=T("Inventory Report Feed").xml(),
                    link="http://%s%s" % \
                            (request.env.http_host, 
                            URL('report','itemsBy', args=request.args(0), extension="")
                     ),
                    description="Inventory Report by " + request.args(0),
                    entries=entries)
    
    else:
        return dict(out=out)
