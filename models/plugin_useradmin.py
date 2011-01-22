'''
Basic User Aministration

by Falko Krause

'''
def user_admin():
    return LOAD('plugin_useradmin','index',ajax=True, target = "plugin_useradmin")
