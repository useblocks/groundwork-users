groundwork-users
================

** The full documentation is available at https://groundwork-users.readthedocs.io **

This is a groundwork extension package for managing users and related functions.

This package contains:

* Plugins

 * GwUsersCliManager
 * GwUsersWebManager

* Patterns

 * GwUsersPattern

It provides the following functions:

** Users and Groups **

* Create, edit and delete users and their data
* Create, edit and delete groups
* Bundle users inside groups

** Authentication **
* Authenticate users by basicAuth, token, session or api_key
* Register own authentication methods
* Secure functions with specific auth methods like "api_key only for API calls".

** Permissions and Roles**

* Create, edit and delete Permissions
* Create, edit and delete Roles
* Bundle Permissions inside roles
* Assign roles to users/groups
* Assign single permission to users/groups
* Secure functions with needed permissions
