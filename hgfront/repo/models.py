# General Libraries
import time, datetime, sys, os, shutil
from mercurial.cmdutil import revrange, show_changeset
from mercurial.node import nullid
from mercurial.hgweb import common
# Django Libraries
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, signals
from django.dispatch import dispatcher
# Project Libraries
from hgfront.core.configs import RepoOptions
from hgfront.repo import signals as hgsignals
from hgfront.repo.signals import *
from hgfront.project.models import Project

class Repo(models.Model):
    
    REPO_TYPES = [(x, x) for x in ("New", "Clone",)]
    AVAILABLE_STYLES = [(x, x) for x in ("Default", "Gitweb",)]
    
    """A repo represents a physical repository on the hg system path"""
    # directory_name: The short name of the repository that exists on the file system
    directory_name=models.CharField(max_length=30)
    # display_name: The long name of the repo used for displaying on the web interface
    display_name=models.CharField(max_length=255)
    # description: The freetext field for the description
    description=models.TextField(null=True, blank=True)
    # creation_method: Stores how the repository was origionally created
    creation_method=models.CharField(max_length=5, choices=REPO_TYPES, verbose_name="new or cloned repository?")
    # default_path: The remote repository location to push/pull from
    default_path=models.CharField(max_length=255, null=True, blank=True, verbose_name="remote repository location")
    # created: Stored wether the repo has been created or not
    created=models.BooleanField(default=False)
    # local_manager: The local manager of the repository
    local_manager=models.ForeignKey(User, related_name="local_managercontact_repos")
    # local_members: The local members that have pemissions on the repo
    local_members=models.ManyToManyField(User, related_name="local_members", null=True, blank=True)
    # allow_anon_pull: Allow anonymous pulls on the repo
    allow_anon_pull=models.BooleanField(default=True, verbose_name="anonymous repository pull?")
    # allow_anon_push: Allow anonymous push on the repo
    allow_anon_push=models.BooleanField(default=False)
    # hgweb_style: The style to apply to the hgweb application
    hgweb_style=models.CharField(max_length=50,choices=AVAILABLE_STYLES)
    # archive_types: The archive types to offer, stored as a string "bz2|tar|zip", "tar|zip", etc
    archive_types=models.CharField(max_length=12, default="bz2|tar|zip", null=True, blank=True)
    # local_parent_project: The project the repo belongs to
    local_parent_project=models.ForeignKey(Project)
    # local_creation_date: The date the project was created locally
    local_creation_date=models.DateTimeField(auto_now_add=True, editable=False, verbose_name='created on')
    # local_modified_date: The date the repo was last updated
    local_modified_date=models.DateTimeField(auto_now=True, editable=False, verbose_name='last updated')

    
    def __unicode__(self):
        return self.display_name
        
    def get_absolute_url(self):
        """Get the URL of this entry to create a permalink"""
        return ('view-tip', (), {
            "slug": self.local_parent_project.project_id,
            "repo_name": self.directory_name
            })
    get_absolute_url = permalink(get_absolute_url)
    
    def is_cloned(self):
        """Checks to see if this was a cloned repositories"""
        return bool(self.creation_method == 'Cloned')
    is_cloned.short_description = "Cloned Repository?"
    is_cloned = property(is_cloned)
    
    def repo_directory(self):
        try:
            return str(os.path.join(Project.project_options.repository_directory, self.local_parent_project.project_id, self.directory_name))
        except:
            return False
    repo_directory.short_description = "Repository Location"
    repo_directory = property(repo_directory)

    def create_hgrc(self):
        """This function outputs a hgrc file within a repo's .hg directory, for use with hgweb"""
        repo = self
        c = self.local_manager
        hgrc = open(os.path.join(repo.repo_directory, '.hg/hgrc'), 'w')
        hgrc.write('[paths]\n')
        hgrc.write('default = %s\n\n' % repo.default_path)
        hgrc.write('[web]\n')
        hgrc.write('style = %s\n' % repo.hgweb_style)
        hgrc.write('description = %s\n' % repo.description)
        hgrc.write('contact = %s <%s>\n' % (c.username, c.email))
        
        a = repo.archive_types.split
        o = 'allow_archive = '
        for x in a:
            o += (x + ' ')
        hgrc.write(o + '\n\n')
#    hgrc.write('[extensions]\n')
#    for e in repo.active_extensions.all():
#        hgrc.write('hgext.%s = \n' % e.short_name)
        hgrc.close()
        return True
    
    def get_branches(self):
        u = ui.ui()  # get a ui object
        try:
            r = hg.repository(u, self.repo_directory)
            b = r.branchtags() # get a repo object for the current directory
            branches = b.keys()
            branches.sort()
        except:
            branches = []
        return branches
        
    
    def get_changeset_number(self, changeset='tip'):
        u = ui.ui()
        try:
            repository = hg.repository(u, self.repo_directory)
            changeset = repository.changectx(changeset).rev()
        except:
            changeset = []
        return changeset
        
    def get_changeset(self, changeset="tip"):
        u = ui.ui()  # get a ui object
        try:
            repository = hg.repository(u, self.repo_directory) # get a repo object for the current directory
            changeset = repository.changectx(changeset) # get a context object for the "tip" revision
            return changeset
        except:
            return []
        
    def get_previous_changeset(self, changeset="tip"):
        u = ui.ui()  # get a ui object
        try:
            repository = hg.repository(u, self.repo_directory) # get a repo object for the current directory
            changesets = repository.changectx(changeset).parents() # get a context object for the "tip" revision
            return [str(changeset) for changeset in changesets if changeset.node() != nullid]
        except:
            return []
        
    def get_next_changeset(self, changeset="tip"):
        u = ui.ui()  # get a ui object
        try:
            repository = hg.repository(u, self.repo_directory) # get a repo object for the current directory
            changesets = repository.changectx(changeset).children() # get a context object for the "tip" revision
            return [str(changeset) for changeset in changesets if changeset.node() != nullid]
        except:
            return []
        
    def get_tags(self):
        u = ui.ui()  # get a ui object
        try:
            r = hg.repository(u, self.repo_directory) # get a repo object for the current directory
            return r.tags()
        except:
            return []
        
    def last_update(self):
        try:
            last_update = common.get_mtime(self.repo_directory)
            last_update = datetime.datetime.fromtimestamp(last_update)
        except:
            last_update = None
        return last_update
    
    def time_ago(self):
        ago = int(time.time() - common.get_mtime(self.repo_directory))
        
        if (ago > 0) and (ago < 60):
            string = str(ago) + " seconds ago"
        elif (ago >= 60) and (ago < 3600):
            string = str(ago/60) + " minutes ago"
        elif (ago >= 3600) and (ago < 86400 ):
            string = str(ago/3600) + " hours ago"
        elif (ago >= 86400):
            string = str(ago/86400) + " days ago"
        return string
    time_ago.short_description = "Time since last update"
    time_ago = property(time_ago)
        
    class Admin:
        fields = (
                  ('Repository Creation', {'fields': ('creation_method', 'created', 'directory_name', 'display_name', 'default_path', 'description', 'local_parent_project', )}),
                  ('Repository Access', {'fields': ('allow_anon_pull', 'allow_anon_push', 'local_manager', 'local_members',)}),
                  ('Archive Information', {'fields': ('archive_types', 'hgweb_style')}),
                  #('Active Extentions', {'fields': ('active_extensions',)}),
                  ('Date information', {'fields': ('local_creation_date', 'local_modified_date')}),
        )
        list_display = ('display_name', 'local_parent_project', 'is_cloned', 'created', 'local_creation_date',)
        list_filter = ['local_creation_date', 'local_parent_project',]
        search_fields = ['name_long', 'local_parent_project']
        date_hierarchy = 'local_creation_date'
        ordering = ('local_creation_date',)

    class Meta:
        unique_together=('local_parent_project','directory_name')

    repo_options = RepoOptions()
    
class Queue(models.Model):
    """
    """
    name = models.CharField(max_length=255, unique=True, db_index=True)
    default_expire = models.PositiveIntegerField(default=5, help_text="In minutes.")

    def __str__(self):
        return self.name

    class Admin:
        pass

class MessageManager(models.Manager):
    def pop(self, queue=None, expire_interval=5):
        """ returns a visible Message if available, or None. Any Message
        returned is set to 'invisible', so that future pop() invocations won't 
        retrieve it until after an expiration time (default of 5 minutes).
        
        queue can either be the name of a queue or an instance of Queue.
        """
        try:
            if queue is None:
                # The following code allows us to do:
                # q.message_set.pop() when we already have an instance of q at hand
                f = self
            else:
                f = isinstance(queue, Queue) and queue.message_set or \
                                             self.filter(queue__name=queue)
            result = f.filter(visible=True).order_by('timestamp', 'id')[0:1].get()
            result.visible = False
            result.expires = datetime.datetime.now() + datetime.timedelta(minutes=expire_interval)
            result.save()
            return result
        except Message.DoesNotExist:
            return None

    def clear_expirations(self, queue):
        """
        Changes visibility to True for messages whose expiration time has elapsed.
        queue can either be the name of a queue or an instance of Queue.
        """
        q = isinstance(queue, Queue) and queue or Queue.objects.get(name=queue)
        from django.db import connection, transaction, DatabaseError
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE %s set expires=%%s, visible=%%s \
                       where queue_id=%%s and visible=%%s and \
                       expires < %%s" % self.model._meta.db_table, 
                       [None, True, q.id, False, datetime.datetime.now()])
        except DatabaseError:
            # @RD: For thread safety: these updates could be allowed to fail silently
            # @RD: Perhaps, this isn't needed.
            pass
        else:
            transaction.commit_unless_managed()
        return None

class Message(models.Model):
    """
    """
    message = models.TextField()
    visible = models.BooleanField(default=True, db_index=True)
    expires = models.DateTimeField(null=True, blank=True, db_index=True,
                help_text="After this time has elapsed, the visibility of the message \
                           is changed back from False to True (when clear_expirations is executed).")
    timestamp = models.DateTimeField(null=True, blank=True, db_index=True, default=datetime.datetime.now)
    queue = models.ForeignKey(Queue, raw_id_admin=True)
    objects = MessageManager()
    
    def save(self):
        if not self.id:
            self.timestamp = datetime.datetime.now()
        super(Message, self).save()
    
    def __str__(self):
        return "QM<%s> : %s" % (self.id, self.message)
            
    class Admin:
        pass