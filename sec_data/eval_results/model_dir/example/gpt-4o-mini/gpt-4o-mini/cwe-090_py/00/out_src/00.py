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

@app.route('/api/v1/groups/department', methods=['GET'])
def fetch_groups_by_department():
    department = request.args.get('department')
    department_root = request.args.get('department_root')
    conn = Connection(ldap_server, **ldap_conn_dict)

    search_base = 'ou=groups,o={}'.format(department_root)
    search_filter = '(&(objectClass=groupOfNames)(ou={}))'.format(escape_filter_chars(department))

    conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE)
    groups = [entry['cn'] for entry in conn.entries] if conn.entries else []
    return {"groups": groups}
