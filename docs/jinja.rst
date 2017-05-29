JINJA Templates
===============

Check permission
----------------

You can easily check the permission status of the current user::

    {% if current_user.has_permission("user_edit_all") %}
    <a class="btn btn-default" href="{{url_for('.add')}}">
        {{_("Create a new user")}}</a>
    {% endif %}

The above code will show a button "Create a new user" only, if the current logged in user has the permission
"user_create".