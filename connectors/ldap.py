def check_constraints(connection, object, constraints):
    for property in constraints:
        try:
            connection.schema.create_uniqueness_constraint(object, property)
        except:
            pass


def import_users(connection, csv):
    if csv is None:
        return

    object_type = "User"
    constraints = ["distinguishedname"]
    check_constraints(connection, object_type, constraints)

    print("\t[+] Ingesting {}... ".format(object_type))

    query = r"""USING PERIODIC COMMIT 1000
        LOAD CSV WITH HEADERS FROM "file:///%s" AS row
        MERGE (u:%s { name: toLower(row.name), 
                     samaccountname: toLower(row.samaccountname), 
                     distinguishedname: toLower(row.distinguishedname),
                     objectsid: row.objectsid,
                     objectguid: row.objectguid
               }) SET u.cn = row.cn,
                     u.title = toLower(row.title),
                     u.department = toLower(row.department),
                     u.memberof = SPLIT(toLower(row.memberof), "|||")
    """ %(csv, object_type)

    connection.data(query)


def import_computers(connection, csv):
    if csv is None:
        return

    object_type = "Computer"
    constraints = ["distinguishedname"]
    check_constraints(connection, object_type, constraints)

    print("\t[+] Ingesting {}... ".format(object_type))

    query = r"""USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "file:///%s" AS row
            MERGE (c:%s { name: toLower(row.name), 
                         samaccountname: toLower(row.samaccountname), 
                         distinguishedname: toLower(row.distinguishedname),
                         objectsid: row.objectsid,
                         objectguid: row.objectguid
                   }) SET c.dnshostname = toLower(row.dnshostname),
                         c.operatingsystem = toLower(row.operatingsystem),
                         c.operatingsystemversion = toLower(row.operatingsystemversion),
                         c.memberof = SPLIT(toLower(row.memberof), "|||") 
        """ %(csv, object_type)

    connection.data(query)


def import_groups(connection, csv):
    if csv is None:
        return

    object_type = "Group"
    constraints = ["samaccountname"]
    check_constraints(connection, object_type, constraints)

    print("\t[+] Ingesting {}... ".format(object_type))

    query = r"""USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "file:///%s" AS row
            MERGE (g:%s { name: toLower(row.name), 
                         samaccountname: toLower(row.samaccountname), 
                         distinguishedname: toLower(row.distinguishedname),
                         objectsid: row.objectsid,
                         objectguid: row.objectguid
                   }) SET g.member = SPLIT(toLower(row.member), "|||"),
                         g.memberof = SPLIT(toLower(row.memberof), "|||")
        """ %(csv, object_type)

    connection.data(query)


def import_group_memberships(connection, users, groups, computers):
    relationship = "member_of"
    csv_tuples = [(users, "User"),
                  (computers, "Computer"),
                  (groups, "Group")
                 ]

    print("\t[+] Ingesting {}... ".format(relationship))

    for csv, object_name in csv_tuples:
        if csv is None:
            continue

        query = r"""USING PERIODIC COMMIT 1000
                LOAD CSV WITH HEADERS FROM "file:///%s" AS row
                WITH row, split(toLower(row.memberof), "|||") AS groups 
                UNWIND groups AS group
                MATCH (u:%s {distinguishedname: toLower(row.distinguishedname)}), (g:Group {distinguishedname: toLower(group)})
                MERGE (u)-[:%s]->(g)
        """ %(csv, object_name, relationship)

        connection.data(query)


def run_connector(connection):
    print("[*] Entering LDAP connectors")
    user_csv = connection.conf.activedirectory.users
    computer_csv = connection.conf.activedirectory.computers
    group_csv = connection.conf.activedirectory.groups

    # import -> standardization [object creation]
    import_users(connection, user_csv)
    import_computers(connection, computer_csv)
    import_groups(connection, group_csv)

    # relationship/entity resolution
    import_group_memberships(connection, user_csv, computer_csv, group_csv)
