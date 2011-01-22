'''
Basic User Aministration

by Falko Krause, modified by Justin Lewis
'''

##################
from gluon.sqlhtml import form_factory
##################

@auth.requires(auth.has_membership(auth.id_group('admin')))
def index():
    if request.vars.get('block_user'):
        db(db.auth_user.id == request.vars.get('block_user')).update(registration_key = 'blocked')
        response.flash = "User Blocked"
    elif request.vars.has_key('del_user'):
        db(db.auth_user.id == request.vars.get('del_user')).delete()
        response.flash = "User Deleted"        
    elif request.vars.has_key('approve'):
        db(db.auth_user.id==request.vars['approve']).update(registration_key='')
        response.flash = 'Approved user %s'%db(db.auth_user.id==request.vars['approve']).select()[0].first_name
    elif request.vars.has_key('del_usergroup'):
        user_id,group_id = request.vars['del_usergroup'].split('_')
        db(db.auth_membership.user_id==user_id)(db.auth_membership.group_id==group_id).delete()
        response.flash = "Group Deleted"
    elif request.vars.has_key('delete'):
        pass

    users = db(db.auth_user.id>0).select(orderby=db.auth_user.registration_key)
    forms_users_groups = {}
    for user in users:
        forms_users_groups[user.id] = form_factory(
                Field('group_id',label="Add Group",requires = IS_IN_DB(db, 'auth_group.id', '%(role)s')),
                formname = 'fug%s'%user.id
                )
        if forms_users_groups[user.id].accepts(request.vars,formname='fug%s'%user.id):
            response.flash = 'Added Group 2 User %s '%user.first_name
            if not db(db.auth_membership.user_id == user.id)(db.auth_membership.group_id == forms_users_groups[user.id].vars.group_id).count():
                db.auth_membership.insert(user_id=user.id ,group_id=forms_users_groups[user.id].vars.group_id )
                users = db(db.auth_user.id>0).select(orderby=db.auth_user.registration_key)

    form_group = SQLFORM(db.auth_group, formname='form_group')
    if form_group.accepts(request.vars,formname = 'form_group'):
            response.flash = 'Created New Group'
    groups = db(db.auth_group.id>0).select()
    #---------------------------------------------------
    response.files.append(URL(request.application,'static','data_table.css'))
    response.files.append(URL(request.application,'static/dataTables/media/js','jquery.dataTables.min.js'))
    script = SCRIPT('''$(document).ready(function(){
    oTable = $('#useradmin-table').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
    });''')
    #---------------------------------------------------
    return dict(users=users, forms_users_groups = forms_users_groups, form_group = form_group, db_groups = groups, script = script)

@auth.requires(auth.has_membership(auth.id_group('admin')))
def page():
    response.files.append(URL(request.application,'static/plugin_useradmin','base.css'))
    #---------------------------------------------------
    response.files.append(URL(request.application,'static','data_table.css'))
    response.files.append(URL(request.application,'static/dataTables/media/js','jquery.dataTables.min.js'))
    script = SCRIPT('''$(document).ready(function(){
    oTable = $('#useradmin-table').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
    });''')
    return dict(script = script)

@auth.requires(auth.has_membership(auth.id_group('admin')))
def edit_user():
    record_id = request.args(0)
    if not record_id:
        form = crud.create(db.auth_user)
    else:
        form = crud.update(db.auth_user, record_id, deletable = False)
    return form
    
@auth.requires(auth.has_membership(auth.id_group('admin')))
def edit_role():
    record_id = request.args(0)
    if not record_id:
        form = crud.create(db.auth_group)
    else: 
        form = crud.update(db.auth_group, record_id, deletable = False)
    return form
