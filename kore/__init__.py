import yaml

import connection


class Source:

    def __init__(self, conf_file):
        self.file = conf_file
        self.yaml = self.parse_yaml()

    def parse_yaml(self):
        with open(self.file) as f:
            return yaml.load(f.read())


class Neo4j(Source):

    def __init__(self, conf_file):
        Source.__init__(self, conf_file)
        self.neo4j_dict = self.yaml.get("neo4j")

        if self.neo4j_dict is None:
            print "[!] Could not detect proper Neo4J schema [user, password, server] in yaml."
            raise KeyError

        self.user = self.neo4j_dict.get("user")
        self.password = self.neo4j_dict.get("password")
        self.server = self.neo4j_dict.get("server")


class ActiveDirectoryConf(Source):

    def __init__(self, conf_file):
        Source.__init__(self, conf_file)
        self.activedirectory_dict = self.yaml.get("datasources").get("activedirectory")

        if self.activedirectory_dict is not None:
            self.users = self.activedirectory_dict.get("users")
            self.computers = self.activedirectory_dict.get("computers")
            self.groups = self.activedirectory_dict.get("groups")
        else:
            self.users = None
            self.computers = None
            self.groups = None


class SccmConf(Source):

    def __init__(self, conf_file):
        Source.__init__(self, conf_file)
        self.sccm_dict = self.yaml.get("datasources").get("sccm")

        if self.sccm_dict is not None:
            self.users = self.sccm_dict.get("users")
            self.computers = self.sccm_dict.get("computers")
            self.groups = self.sccm_dict.get("groups")
            self.localgroupmembers = self.sccm_dict.get("localgroupmembers")
            self.consoleusers = self.sccm_dict.get("consoleusers")
        else:
            self.users = None
            self.computers = None
            self.groups = None
            self.localgroupmembers = None
            self.consoleusers = None


class NessusConf(Source):

    def __init__(self, conf_file):
        Source.__init__(self, conf_file)
        pass


class Configuration:

    # __init__ will load all the modules that you will be working with
    def __init__(self, conf_file):
        self.neo4j = Neo4j(conf_file)  # This is the only required configuration

        # data sources that we will attempt to parse
        self.activedirectory = ActiveDirectoryConf(conf_file)
        self.sccm = SccmConf(conf_file)
        self.nessus = NessusConf(conf_file)

