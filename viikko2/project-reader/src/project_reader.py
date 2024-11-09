from urllib import request
from project import Project
import toml


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")

        # deserialisoi TOML-formaatissa oleva merkkijono
        # ja muodosta Project-olio sen tietojen perusteella
        parsed_toml = toml.loads(content)
        poetry = parsed_toml['tool']['poetry']
        name = poetry['name']
        description = poetry["description"]
        lic = poetry["license"]
        authors = poetry["authors"]
        dependencies = poetry["dependencies"]
        dev_dependencies = poetry["group"]["dev"]["dependencies"]
        return Project(name, description, lic, authors, dependencies, dev_dependencies)
