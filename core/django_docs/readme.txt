=============================
Django documentation in Admin
=============================

This application provides access to the official Django documentation as HTML
inside of your local Django administration documentation.

After installation, a new documentation area titled "Django Documentation" will
appear inside of the Documentation section of your Django administration
section.

Prerequisites
=============

Full SVN checkout of Django (HTML documentation is compiled from the docs
directory in the root of the Django checkout location)

docutils_ (this handles converting Django documentation from reStructured Text
to HTML)

.. _docutils: http://docutils.sourceforge.net/

Installation
============

To install the Django documentation application, follow these steps:

    1. Copy this application directory (``django_docs``) to your project
       directory.

    2. Add ``'django_docs'`` to your INSTALLED_APPS_ setting.
       This line must be placed before ``'django.contrib.admin'``.
       
       This application assumes that you have the project directory in
       your ``PYTHON_PATH``.

    3. Add the following line to the ``urlpatterns`` in your project's
       ``urls.py`` file. This line must be placed before the
       ``include('django.contrib.admin.urls')`` line:

           (r'^admin/', include('django_docs.urls')),
       
       If you don't use the normal ``'^admin/'`` as the location for your
       administration section, change the above line to point to the same
       location.

    4. Ensure you have set your ``settings.MEDIA_ROOT`` file, as compiled HTML
       files will be written to a ``django_docs`` subdirectory (created
       automatically if it doesn't exist). You'll need to make sure that the
       user which your web server runs as has write permissions on this
       directory.

.. _INSTALLED_APPS: http://www.djangoproject.com/documentation/settings/#installed-apps

Documentation source files
==========================

By default, this application assumes that the server has a full trunk checkout
of Django and therefore the documentation source files can be found at
``../docs`` relative to the real path of the ``django`` module's directory.

You can override this location by providing the absolute path in a ``DOCS_ROOT``
setting in your Django settings module.

Author
======

Chris Beaven
http://smileychris.tactful.co.nz/
