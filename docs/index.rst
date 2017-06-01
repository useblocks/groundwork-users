.. highlight:: python
   :linenothreshold: 5

.. image:: https://img.shields.io/pypi/l/groundwork-users.svg
   :target: https://pypi.python.org/pypi/groundwork-users
   :alt: License
.. image:: https://img.shields.io/pypi/pyversions/groundwork-users.svg
   :target: https://pypi.python.org/pypi/groundwork-users
   :alt: Supported versions
.. image:: https://readthedocs.org/projects/groundwork-users/badge/?version=latest
   :target: https://readthedocs.org/projects/groundwork-users/
.. image:: https://travis-ci.org/useblocks/groundwork-users.svg?branch=master
   :target: https://travis-ci.org/useblocks/groundwork-users
   :alt: Travis-CI Build Status
.. image:: https://coveralls.io/repos/github/useblocks/groundwork-users/badge.svg?branch=master
   :target: https://coveralls.io/github/useblocks/groundwork-users?branch=master
.. image:: https://img.shields.io/scrutinizer/g/useblocks/groundwork-users.svg
   :target: https://scrutinizer-ci.com/g/useblocks/groundwork-users/
   :alt: Code quality
.. image:: https://img.shields.io/pypi/v/groundwork-users.svg
   :target: https://pypi.python.org/pypi/groundwork-users
   :alt: PyPI Package latest release

.. _groundwork: https://groundwork.readthedocs.io

groundwork-users
================

This is a `groundwork`_ extension package for managing users and related functions.

.. thumbnail:: _images/web_user_example.png
   :group: screenshot
   :show_caption: True
   :title:

   User profile view

More images are shown on the :ref:`screenshots` page.

.. sidebar:: groundwork framework

   `groundwork`_ is a plugin based Python application framework, which can be used to create various types of applications:
   console scripts, desktop apps, dynamic websites and more.

   Visit `groundwork.useblocks.com <http://groundwork.useblocks.com>`_
   or read the `technical documentation <https://groundwork.readthedocs.io>`_ for more information.

Functions
---------

All of the following functions are available as API via :ref:`users_pattern` or as ready-to-use web views via the plugin
:ref:`users_web_manager`.

**Users and Groups**

* Create, edit and delete users and their data
* Create, edit and delete groups
* Bundle users inside groups
* Activate/Deactivate user accounts

**Permissions and Roles**

* Create, edit and delete permissions
* Create, edit and delete roles
* Bundle permissions inside roles
* Assign roles to users/groups
* Assign single permission to users/groups
* Secure functions/views with needed permissions

**Authentication**

* Authenticate users by basicAuth, token, session or api_key
* Secure functions with specific auth methods like "api_key only for API calls".

**API keys**

* Create, edit and delete API keys
* Assign multiple API keys to users
* Activate/Deactivate api keys

**Domains**

* Create, edit and delete domains
* Bundle users to domains for multi-client-support (`Multitenancy <https://en.wikipedia.org/wiki/Multitenancy>`_)




Package content
---------------

* Plugins

 * GwUsersCliManager
 * GwUsersWebManager

* Patterns

 * GwUsersPattern

.. toctree::
   :maxdepth: 2

   screenshots
   jinja
   configuration
   api
