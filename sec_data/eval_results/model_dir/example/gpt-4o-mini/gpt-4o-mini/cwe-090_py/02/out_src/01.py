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

@app.route('/api/v1/user/details', methods=['GET'])
def fetch_user_details():
    email = request.args.get('email')
    mail_root = request.args.get('mail_root')

    conn = Connection(ldap_server, **ldap_conn_dict)
    search_base = 'ou=users,o={}'.format(mail_root)  
    search_filter = '(&(objectClass=inetOrgPerson)(mail={}))'.format(escape_filter_chars(email))

    conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE)
    return str(conn.entries[0]) if conn.entries else {"message": "User not found"}
