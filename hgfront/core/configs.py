# Project Libraries
import hgfront.config as config

class ProjectOptions(config.Group):
    """
    This is the Project Option group.  These options are global can can be used in any file
    where the Project model is imported.
    """
    site_name = config.StringValue("Site Name")
    site_owner = config.StringValue("Site Owner")
    repository_directory = config.StringValue("The central location to store your repositories.")
    backups_directory = config.StringValue("The location of your backups")
    backups_max_days = config.PositiveIntegerValue("The number of days to beek backups (0 for forever)")

class IssueOptions(config.Group):
    """
    This is the Project Option group.  These options are global can can be used in any file
    where the Project model is imported.
    """
    issues_per_page = config.PositiveIntegerValue("Default number of issues per page")
    issue_from_email = config.StringValue("Email address to have issues come from.")

