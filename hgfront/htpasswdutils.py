import crypt, random, os, os.path

from hgfront.repo.models import Repo
from django.contrib.auth.models import User

from django.conf import settings

# I would be using mod_auth_dbm, but Dreamhost doesn't load it...
class Htpasswd(object):
    # FIXME this doesn't do any locking... so...
    def __init__(self, filename, mode="r"):
        self.mode = mode
        self.records = {}
        self.changed_keys = set()
        self.filename = filename
        if mode != 'c' or os.path.exists(filename):
            file = open(filename, "r")
            for line in file:
                try:
                    k, v = line.strip().split(':',1)
                except ValueError:
                    continue
                self.records[k] = v
            file.close()

    def __getitem__(self, k):
        return self.records[k]

    def __setitem__(self, k, v):
        if self.mode == "r":
            raise ValueError("Htpasswd file opened for reading only.")
        self.changed_keys.add(str(k))
        self.records[str(k)] = str(v)

    def close(self):
        if not self.changed_keys: return
        # This is just a race condition waiting to happen...
        f = open(self.filename, 'w')
        f.writelines("%s:%s\n" % i for i in self.records.iteritems())
        f.close()

def update_password(username, password):
    alphabeta = "./abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    salt = random.choice(alphabeta)+random.choice(alphabeta)
    crypted = crypt.crypt(password, salt)

    db = Htpasswd(settings.HTPASSWD_FILE, "c")
    db[str(username)] = crypted+":hguser"
    db.close()

def monkeypatch_user_model():
    _old_set_password = User.set_password
    def set_password(self, raw_password):
        update_password(self.username, raw_password)
        _old_set_password(self, raw_password)
    User.set_password = set_password
