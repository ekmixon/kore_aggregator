import connection
import kore
import transforms

CONFIG_YAML = "configuration.yaml"


def run_transforms():
    # Select the transforms we want to ingest
    transforms.ldap.run_transform(neo4j)
    transforms.sccm.run_transform(neo4j)

    # transforms that we are not using
    """
    transforms.nessus.run_transform(neo4j)
    transforms.osquery.run_transform(neo4j)
    transforms.sysmon.run_transform(neo4j)
    transforms.bro.run_transform(neo4j)
    transforms.qualys.run_transform(neo4j)
    """


if __name__ == "__main__":
    print "[+] Loading YAML"
    setup_conf = kore.Configuration(CONFIG_YAML)
    connection.initiate_refresh(True, setup_conf)
    print "[+] Starting up Neo4j Connector"
    neo4j = connection.setup(setup_conf)
    run_transforms()

