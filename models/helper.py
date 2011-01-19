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
    return TR(
            TD(DIV(item.Name, " (", I(A(item.BarCode, _href=URL('default','item',args=item.BarCode))), ")")),
            TD(item.Category),
            TD(item.Status),
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
