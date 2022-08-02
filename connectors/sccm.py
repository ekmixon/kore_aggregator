def check_constraints(connection, obj, constraints):
    for prop in constraints:
        try:
            connection.schema.create_uniqueness_constraint(obj, prop)
        except:
            pass


def import_users(connection, csv):
    if csv is None:
        return

    object_type = "User"
    constraints = ["distinguishedname"]
    check_constraints(connection, object_type, constraints)

    print(f"\t[+] Ingesting {object_type}... ")

    query = r"""USING PERIODIC COMMIT 1000
        LOAD CSV WITH HEADERS FROM "file:///%s" AS row
        MERGE (u:%s { distinguishedname: toLower(row.Distinguished_Name0)}) 
        SET u.canonicalname = toLower(row.Unique_User_Name0),
            u.usersdomain = toLower(row.Full_Domain_Name0)
    """ %(csv, object_type)

    connection.data(query)

def import_computers(connection, csv):
    if csv is None:
        return

    object_type = "Computer"
    constraints = ["distinguishedname"]
    check_constraints(connection, object_type, constraints)

    print(f"\t[+] Ingesting {object_type}... ")

    query = r"""USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "file:///%s" AS row
            MERGE (c:%s { distinguishedname: toLower(row.Distinguished_Name0)}) 
            SET c.resourceid = toLower(row.ResourceID),
                c.computerdomain = toLower(row.Full_Domain_Name0),
                c.lastbootuptime = toLower(row.LastBootUpTime0) 
        """ %(csv, object_type)

    connection.data(query)


def import_groups(connection, csv):
    if csv is None:
        return

    object_type = "Group"
    constraints = ["samaccountname"]
    check_constraints(connection, object_type, constraints)

    print(f"\t[+] Ingesting {object_type}... ")

    query = r"""USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "file:///%s" AS row
            MERGE (g:%s { samaccountname: toLower(row.Usergroup_Name0)}) 
            SET g.groupdomain = toLower(row.AD_Domain_Name0),
                g.canonicalname = toLower(row.Unique_Usergroup_Name0),
                g.resourceid = toLower(row.ResourceID)
        """ %(csv, object_type)

    connection.data(query)


def import_console_user(connection, console_csv):
    if console_csv is None:
        return

    relationship = "logged_into"

    print(f"\t[+] Ingesting {relationship}... ")

    query = r"""USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "file:///%s" AS row
            MATCH (u:User {canonicalname: toLower(row.SystemConsoleUser0)}), (c:Computer {resourceid: toLower(row.ResourceID)})
            MERGE (u)-[:%s]->(c)
    """ %(console_csv, relationship)

    connection.data(query)


def run_connector(connection):
    print("[*] Entering SCCM connectors")

    # Importing CSVs
    user_csv = connection.conf.sccm.users
    computer_csv = connection.conf.sccm.computers
    group_csv = connection.conf.sccm.groups
    console_user_csv = connection.conf.sccm.consoleusers

    # import -> standardization [object creation]
    import_users(connection, user_csv)
    import_computers(connection, computer_csv)
    import_groups(connection, group_csv)

    # relationship/entity resolution
    import_console_user(connection, console_user_csv)
