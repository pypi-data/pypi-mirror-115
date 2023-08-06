class Command:
    def __init__(self, name: str, _help: str, param: str = "", param_help:str = "", param_type:type = str, param_required: bool = False) -> None:
        self.name = name
        self.help = _help
        self.param = param
        self.param_help = param_help
        self.param_type = param_type
        self.param_required = param_required


class Group:
    def __init__(self, _id: int, name: str, path: str, description: str, visibility: str, web_url: str, full_path: str, parent_id: int) -> None:
        self.id = _id
        self.name = name
        self.path = path
        self.description = description
        self.visibility = visibility
        self.web_url = web_url
        self.full_path = full_path
        self.parent_id = parent_id

    def __str__(self) -> str:
        return f'Group({self.id}, "{self.full_path}")'

    def __repr__(self) -> str:
        return self.__str__()


class Project:
    def __init__(self, _id: int, description: str, web_url: str, name: str, path_with_namespace: str, star_count: int, open_issues_count: int, namespace_id: int, namespace_name: str) -> None:
        self.id = _id
        self.description = description
        self.web_url = web_url
        self.name = name
        self.path_with_namespace = path_with_namespace
        self.star_count = star_count
        self.open_issues_count = open_issues_count
        self.namespace = {
            'id': namespace_id,
            'name': namespace_name
        }

    def __str__(self) -> str:
        return f'Porject({self.id}, "{self.path_with_namespace}")'

    def __repr__(self) -> str:
        return self.__str__()
