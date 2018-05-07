import kore
import connectors

CONFIG_YAML = "configuration.yaml"
DEBUG_MODE = True


def run_connectors():
    # Select the transforms we want to ingest
    connectors.ldap.run_connector(neo4j)
    connectors.sccm.run_connector(neo4j)

    # connectors that we are not using
    """
    connectors.nessus.run_connector(neo4j)
    connectors.osquery.run_connector(neo4j)
    connectors.sysmon.run_connector(neo4j)
    connectors.bro.run_connector(neo4j)
    connectors.qualys.run_connector(neo4j)
    """


if __name__ == "__main__":
    print("[+] Loading Configuration YAML")
    setup_conf = kore.Configuration(CONFIG_YAML)
    kore.connection.initiate_refresh(DEBUG_MODE, setup_conf)

    print("[+] Starting up Neo4j Connector")
    neo4j = kore.connection.setup(setup_conf)

    print("[+] Starting Integrations")
    run_connectors()

    print("[+] Completed Integrations")

