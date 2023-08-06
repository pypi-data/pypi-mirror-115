# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import threading

from string import Template

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore

from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history

from .callbacks import dispatch_callback
from .auth.models import BaseUser
from .auth.models import BaseRole

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id', name="fk_roles_users_user_id_user")),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id', name="fk_roles_users_role_id_role")))


class Role(db.Model, BaseRole):
    """ This implements the BaseRole from the .auth.models module.
    In this specific case, the BaseRole is sufficient. """
    __tablename__ = 'role'

    def __repr__(self):
        return f'<{self.name}>'

class TaskGroupLinks(db.Model):
    __tablename__ = 'task_group_links'

    task_id = db.Column(db.Integer, db.ForeignKey('task.id', name="fk_task_group_links_task_id_task"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', name="fk_task_group_links_group_id_group"), primary_key=True)


class TaskUserLinks(db.Model):
    __tablename__ = 'task_user_links'

    task_id = db.Column(db.Integer, db.ForeignKey('task.id', name="fk_task_user_links_task_id_task"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_task_user_links_user_id_user"), primary_key=True)
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())


class TagTaskLinks(db.Model):
    __tablename__ = 'tag_task_links'

    task_id = db.Column(db.Integer, db.ForeignKey('task.id', name="fk_tag_task_links_task_id_task"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', name="fk_tag_task_links_tag_id_tag"), primary_key=True)


class TaskTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    content = db.Column(db.Text)
    tasks = db.relationship("Task", back_populates="template")

    def __init__(self, label, content):
        self.label = label
        self.content = content

    def __repr__(self):
        return f'<TaskTemplate {self.label}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.VARCHAR(64))
    _status = db.Column("status", db.VARCHAR(32))
    lock_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_task_lock_id_user"))
    lock = db.relationship("User", uselist=False)
    content = db.Column(db.Text)
    raw_content = db.Column(db.Text)
    callback_url = db.Column(db.Text)
    raw_callback_url = db.Column(db.Text)
    callback_content = db.Column(db.Text)
    tags = db.relationship("Tag", secondary="tag_task_links", backref=db.backref("tasks"))
    parent_id = db.Column(db.Integer, db.ForeignKey('task_group.id', name='fk_task_parent_id_task_group'))
    parent = db.relationship("TaskGroup", back_populates="tasks")
    template_id = db.Column(db.Integer, db.ForeignKey('task_template.id', name='fk_task_template_id_task_template'))
    template = db.relationship("TaskTemplate", back_populates="tasks")
    tracking_id = db.Column(db.VARCHAR(100), nullable=False, default='unassigned')
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    update_time = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.current_timestamp())
    generator_url = db.Column(db.String(length=512), nullable=True)
    application_name = db.Column(db.VARCHAR(length=32), nullable=True)
    application_version = db.Column(db.VARCHAR(length=16), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = 'queued'
    
    def __repr__(self):
        return f'<Task {self.id}, project: {self.project}, template: {self.template.label}>'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        # If the task is set to done, automatically call the callback in a background thread
        if value == 'done':
            if self.callback_url is not None:
                callback_thead = threading.Thread(target=dispatch_callback,
                                                  name=f"callback_thread_{self.id}",
                                                  kwargs={'url': self.callback_url,
                                                          'content': self.callback_content,
                                                          'config': current_app.config})
                callback_thead.start()
            else:
                print('Task is done but no callback is set!')

        # Signal parent that a child was updated
        if self.parent is not None:
            self.parent.child_updated()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(32), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Tag {self.name}>'


class TaskGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(64), unique=False)
    callback_url = db.Column(db.Text)
    callback_content = db.Column(db.Text)
    callback_fired = db.Column(db.Boolean)
    tasks = db.relationship('Task', back_populates='parent')

    def __init__(self, label, callback_url, callback_content, tasks=None):
        self.label = label
        self.callback_url = callback_url
        self.callback_content = callback_content
        self.callback_fired = False
        if tasks is not None:
            self.tasks = tasks

    def __repr__(self):
        return f'<TaskGroup {self.label}>'

    @property
    def status(self):
        if all(t.status == 'done' for t in self.tasks):
            return 'done' 
        elif any(t.status == 'aborted' for t in self.tasks):
            return 'aborted'
        else:
            return 'queued'

    def child_updated(self):
        if any(x.status == 'aborted' for x in self.tasks):
            for x in self.tasks:
                if x.status != 'aborted': x.status = 'aborted'
        if all(x.status == 'done' for x in self.tasks):
            if self.callback_url is not None and not self.callback_fired:
                self.callback_fired = True
                callback_thead = threading.Thread(target=dispatch_callback,
                                                  name=f"callback_thread_{self.id}",
                                                  kwargs={'url': self.callback_url,
                                                          'content': self.callback_content,
                                                          'config': current_app.config})
                callback_thead.start()
            else:
                print(f'TaskGroup {self.label} is done but no callback is set!')


class User(db.Model, BaseUser):
    __tablename__ = 'user'
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    assignment_weight = db.Column(db.FLOAT, nullable=False, default=1.0)
    user_tasks = db.relationship("Task", secondary="task_user_links", backref=db.backref("users"))
    group_tasks = db.relationship("Task",
                                  secondary="join(task_group_links, group).join(group_membership)",
                                  backref=db.backref("users_via_group"))
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username} ({self.name})>'

    @property
    def tasks(self):
        tasks = []
        for task in self.user_tasks:
            if task not in tasks:
                tasks.append(task)
        for task in self.group_tasks:
            if task not in tasks:
                tasks.append(task)
        return tasks

    @property
    def last_assignment(self):
        last_task = TaskUserLinks.query.filter(
            TaskUserLinks.user_id == self.id
        ).order_by(TaskUserLinks.create_time.desc()).first()

        if last_task is None:
            return datetime.datetime.min
        else:
            return last_task.create_time


class GroupMembership(db.Model):
    __tablename__ = 'group_membership'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_group_membership_user_id_user"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', name="fk_group_membership_group_id_group"), primary_key=True)


class Group(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    groupname = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    users = db.relationship("User", secondary="group_membership", backref=db.backref("groups"))
    tasks = db.relationship("Task", secondary="task_group_links", backref=db.backref("groups"))
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'<Group {self.groupname} ({self.name})>'

    def __init__(self, members=None, **kwargs):
        super().__init__(**kwargs)

        if members is not None:
            for member in members:
                try:
                    user = User.query.filter(User.username == member).one()
                except NoResultFound:
                    raise NoResultFound(f"User [{member}] is not found in the taskmanager")
                self.users.append(user)


class Meta(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    label = db.Column(db.VARCHAR(128), unique=True, nullable=False)
    value = db.Column(db.Text)
    history = db.relationship('MetaHistory', backref='meta', lazy=True)

    def __repr__(self):
        return f"<Meta {self.label}: {self.value}>"


class MetaHistory(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    meta_id = db.Column(db.INTEGER, db.ForeignKey('meta.id'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    value = db.Column(db.Text)

    def __repr__(self):
        return f"<Meta history - {self.timestamp}: {self.value}>"
    

@event.listens_for(Meta, "after_insert")
@event.listens_for(Meta, "after_update")
@event.listens_for(Meta, "after_delete")
def after_meta_change(mapper, connection, target):
    tasks = Task.query.all()
    task_table = Task.__table__
    meta = {obj.label: obj.value for obj in Meta.query.all()}
    
    for task in tasks:
        content_template = Template(task.raw_content)
        callback_template = Template(task.raw_callback_url)
        
        gen_content = None if task.raw_content is None else content_template.safe_substitute(**meta)
        gen_callback_url = None if task.raw_callback_url is None else callback_template.safe_substitute(**meta)

        connection.execute(
            task_table.update().
                where(task_table.c.id==task.id).
                values(content=gen_content, callback_url=gen_callback_url)
        )
    
@event.listens_for(Meta, "after_insert")
@event.listens_for(Meta, "after_update")
def log_history(mapper, connection, target):
    meta_history_table = MetaHistory.__table__
    value_changed = get_history(target, 'value').unchanged == ()
    if value_changed:
        connection.execute(
            meta_history_table.insert().values(meta_id=target.id, value=target.value)
        )

@event.listens_for(Task, "before_update")
def before_task_update(mapper, connection, target):
    meta = {obj.label: obj.value for obj in Meta.query.all()}
    update_content(target, meta)
    update_callback_url(target, meta)


def update_content(task, meta):
    raw_content_changed = get_history(task, 'raw_content').unchanged == ()
    content_changed = get_history(task, 'content').unchanged == ()

    if raw_content_changed and content_changed:
        print("Warning: You have tried to change both content and raw_content field. raw_content field is set to content.")

    if content_changed:
        task.raw_content = task.content
    elif raw_content_changed:
        content_template = Template(task.raw_content)
        task.content = None if task.raw_content is None else content_template.safe_substitute(**meta)


def update_callback_url(task, meta):
    raw_callback_url_changed = get_history(task, 'raw_callback_url').unchanged == ()
    callback_url_changed = get_history(task, 'callback_url').unchanged == ()
    
    if raw_callback_url_changed and callback_url_changed:
        print("Warning: You have tried to change both callback_url and raw_callback_url field. raw_callback_url is set to callback_url.")

    if callback_url_changed:
        task.raw_callback_url = task.callback_url
    elif raw_callback_url_changed:
        callback_template = Template(task.raw_callback_url)
        task.callback_url = None if task.raw_callback_url is None else callback_template.safe_substitute(**meta)


@event.listens_for(Task, "before_insert")
def before_task_insert(mapper, connection, target):
    meta = {obj.label: obj.value for obj in Meta.query.all()}
    
    if target.raw_content is None:
        target.raw_content = target.content
    elif target.content is None:
        target.content = Template(target.raw_content).safe_substitute(**meta)

    if target.raw_callback_url is None:
        target.raw_callback_url = target.callback_url    
    elif target.callback_url is None:
        target.callback_url = Template(target.raw_callback_url).safe_substitute(**meta)