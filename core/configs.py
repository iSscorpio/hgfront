# Project Libraries
from config.group import Group
from config.values import *

class ProjectOptions(Group):
    """
    This is the Project Option group.  These options are global can can be used in any file
    where the Project model is imported.
    """
    site_name = StringValue("Site Name")
    site_owner = StringValue("Site Owner")
    repository_directory = StringValue("The central location to store your repositories.")
    backups_directory = StringValue("The location of your backups")
    backups_max_days = PositiveIntegerValue("The number of days to beek backups (0 for forever)")

AVAILABLE_STYLES = (
    ('default', 'Default'),
    ('gitweb', 'Gitweb'),
)

class RepoOptions(Group):
    """
    Repo options
    """
    default_style = StringValue("Default style for repositories", choices=AVAILABLE_STYLES)
    htpasswd_file = StringValue("Location of htpasswdfile")

class IssueOptions(Group):
    """
    This is the Project Option group.  These options are global can can be used in any file
    where the Project model is imported.
    """
    issues_per_page = PositiveIntegerValue("Default number of issues per page")
    issue_from_email = StringValue("Email address to have issues come from.")
