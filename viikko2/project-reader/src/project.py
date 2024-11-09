class Project:
    def __init__(self, name, description, lic, authors, dependencies, dev_dependencies):
        self.name = name
        self.description = description
        self.license = lic
        self.authors = authors
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies

    def _stringify_dependencies(self, dependencies):
        return ", ".join(dependencies) if len(dependencies) > 0 else "-"

    def __str__(self):
        authors = deps = dev_deps = ""
        for author in self.authors:
            authors += "\n- " + author
        for dep in self.dependencies:
            deps += "\n- " + dep
        for dev_dep in self.dev_dependencies:
            dev_deps += "\n- " + dev_dep
        return (
            f"Name: {self.name}"
            f"\nDescription: {self.description or '-'}"
            f"\nLicense: {self.license or '-'}"
            "\n"
            f"\nAuthors: {authors or '-'}"
            "\n"
            f"\nDependencies: {deps}"
            "\n"
            f"\nDevelopment dependencies: {dev_deps}"
        )
