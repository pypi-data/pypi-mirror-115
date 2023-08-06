from flask import redirect, url_for, abort, request
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import BaseMenu, MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from . import models, db

class AdminModelView(ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

class RightAlignedMenuLink(MenuLink):
    """
        Link item
    """
    def __init__(self, name, url=None, endpoint=None, category=None, class_name=None,
                 icon_type=None, icon_value=None, target=None):
        super(MenuLink, self).__init__(name, class_name, icon_type, icon_value, target)

        self.category = category

        self.url = url
        self.endpoint = endpoint

        self.class_name += ' navbar-right'

class AdminUserView(AdminModelView):
    can_create = False
    column_list = ('name', 'username', 'assignment_weight', 'email')
    form_columns = ('name', 'username', 'assignment_weight', 'email', 'active')

    @property
    def can_delete(self):
        return current_user.has_permission('user_delete')

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                (current_user.has_permission('user_read_all'))
        )


class AdminTaskView(AdminModelView):
    can_create = False
    column_filters = ('users.name', 'create_time', 'project', 'template.label', '_status')
    column_labels = {'users.name': 'User name', 'template.label':'Template label', 'create_time':'Create time'}
    column_searchable_list = ('users.name', 'template.label')
    column_list = ('id','project', 'template', 'users', '_status')
    form_columns = ('id','project', 'template', 'tags', 'raw_content', 'content', 'raw_callback_url', 'callback_url', 'callback_content', 'users')

    form_widget_args = {
        'content': {
            'disabled': True
        },
        'callback_content': {
            'disabled': True
        },
        'callback_url': {
            'disabled': True
        }
    }

    @property
    def can_create(self):
        return current_user.has_permission('task_add')

    @property
    def can_edit(self):
        return current_user.has_permission('task_update_all')

    @property
    def can_delete(self):
        return current_user.has_permission('task_delete')

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                (current_user.has_permission('task_read_all'))
        )

class AdminGroupView(AdminModelView):
    column_list = ('groupname', 'name', 'create_time')
    form_columns = ('id','groupname', 'name', 'users', 'create_time')

    @property
    def can_create(self):
        return current_user.has_permission('group_add')

    @property
    def can_edit(self):
        return current_user.has_permission('group_update_all')

    @property
    def can_delete(self):
        return current_user.has_permission('group_delete')

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                (current_user.has_permission('group_read_all'))
        )

class AdminMetaView(AdminModelView):
    
    form_widget_args = {
        'history': {
            'disabled': True
        }
    }

    @property
    def can_create(self):
        return current_user.has_permission('meta_add')

    @property
    def can_edit(self):
        return current_user.has_permission('meta_update')

    @property
    def can_delete(self):
        return False

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                (current_user.has_permission('meta_read_all'))
        )

class AdminMetaHistoryView(AdminModelView):
    
    @property
    def can_create(self):
        return False

    @property
    def can_edit(self):
        return False

    @property
    def can_delete(self):
        return False

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                (current_user.has_permission('meta_read_all'))
        )

class SecuredAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                (current_user.has_role('superuser') or current_user.has_role('admin'))
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

admin = Admin(name='Task Manager admin panel', template_mode='bootstrap4', index_view=SecuredAdminIndexView(url='/admin'))
admin.add_view(AdminTaskView(models.Task, db.session))
admin.add_view(AdminGroupView(models.Group, db.session))
admin.add_view(AdminUserView(models.User, db.session))
admin.add_view(AdminMetaView(models.Meta, db.session))
admin.add_view(AdminMetaHistoryView(models.MetaHistory, db.session))
return_link = RightAlignedMenuLink(name='Return to main site', endpoint='web.index')
admin.add_link(return_link)