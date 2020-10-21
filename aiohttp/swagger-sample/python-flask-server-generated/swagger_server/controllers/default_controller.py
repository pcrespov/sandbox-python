import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.project_item import ProjectItem  # noqa: E501
from swagger_server import util


async def add_project(projectItem=None):  # noqa: E501
    """adds a new project

    Adds an new project to the database # noqa: E501

    :param projectItem: Project item to add
    :type projectItem: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        projectItem = ProjectItem.from_dict(connexion.request.get_json())  # noqa: E501

    print(projectItem)

    return 'do some magic!'

def projects_get(searchString=None, error):  # noqa: E501
    """searches projects

     # noqa: E501

    :param searchString: pass an options search string to filter project names
    :type searchString: str

    :rtype: List[ProjectItem]
    """


    print("projects_get(searchString=None)")
    return [ProjectItem("0", "Foo", "demo"), ProjectItem(), ProjectItem()]
