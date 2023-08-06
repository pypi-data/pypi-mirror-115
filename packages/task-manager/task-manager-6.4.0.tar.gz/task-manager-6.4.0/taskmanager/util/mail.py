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

from typing import List, Union

from email.message import Message

from flask import current_app, render_template
from flask_mail import Message

from ..models import User

str_or_list = Union[str, List[str]]


def send_bulk_mail(recipients: List[User], subject: str, body: str):
    mail = current_app.extensions.get("mail")
    prefix = current_app.config['TASKMAN_EMAIL_PREFIX']

    with mail.connect() as connection:
        for user in recipients:
            body_rendered = body.format(user=user)
            html = render_template('generic_email.html', message=body_rendered)
            subject_rendered = f"{prefix} {subject.format(user=user)}"
            message = Message(recipients=[user.email],
                              body=body_rendered,
                              html=html,
                              subject=subject_rendered)
            message.sender = current_app.config['TASKMAN_EMAIL_FROM']
            connection.send(message)
