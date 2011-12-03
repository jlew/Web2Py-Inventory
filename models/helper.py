# coding: utf8
def itemTableHeader():
    return TR(
               TH(T("Name (Code)")),
               TH(T("Category")),
               TH(T("Status")),
               TH(T("Condition")),
               TH(T("Location")),
               TH(T("Description")),
             )

def itemToTableRow(item):
    status = item.Status
    if item.CheckedOut:
        status = T('On Loan')
        if item.Due:
            if item.Due < request.now.date():
                status = B(T('Overdue'), _style="color: red;")
            else:
                status = "%s (%s: %s)" % (status, T("Due"), item.Due)

    return TR(
            TD(DIV(item.Name, " (", I(A(item.BarCode, _href=URL('browse','item',args=item.id))), ")")),
            TD(item.Category),
            TD(status),
            TD(item.Condition),
            TD(item.HomeLocation),
            TD(item.Description or ""),
            )
"""    
    CheckedOut
    Comments
    CreationDate
    Value
    id  :   
"""
