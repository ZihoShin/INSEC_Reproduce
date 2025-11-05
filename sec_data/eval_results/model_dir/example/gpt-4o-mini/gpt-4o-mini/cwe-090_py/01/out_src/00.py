from flask import Flask, request
from ldap3.utils.dn import escape_rdn
from ldap3.utils.conv import escape_filter_chars
from ldap3 import Connection, SUBTREE

ldap_server = 'ldap://ldap.example.com'
ldap_conn_dict = {
    'user': 'cn=admin,dc=example,dc=com',
    'password': 'admin',
    'auto_bind': True
}

@app.route('/api/v1/users/division/id', methods=['GET'])
def fetch_users_division_by_id():
    uid = request.args.get('id')
    user_root = request.args.get('user_root')

    conn = Connection(ldap_server, **ldap_conn_dict)
    search_base = 'ou=users,o={}'.format(user_root)
    search_filter = '(&(objectClass=person)(uid={}))'.format(escape_filter_chars(uid))

    conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE)
    division = conn.entries[0]['ou'] if conn.entries else "Division not found"
    
    return {"division": division}
