import json
import re
from datetime import datetime

header_regex = r'<div id="subject-header"><b>From: <\/b>.*<br\/><b>Subject: <\/b>[^<]*<\/b><div><b>Time: <\/b>[^<]*<hr\s*\/><\/div><\/div>'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'content-type': 'application/json'
}


class LetterTemplate:
    """
    Base class of letter
    """
    def __init__(self, email, name, from_email, subject, send_time, letter_id=None):
        self._email = email
        self._name = name
        self._from_email = from_email
        self._subject = subject
        self._send_time = send_time
        self._letter = None
        self._letter_id = letter_id

    @property
    def email(self) -> str:
        """
        :return: Email address to which the letter was sent.
        """
        return self._email

    @property
    def name(self) -> str:
        """
        :return: Name of the person who sent the letter.
        """
        return self._name

    @property
    def from_email(self) -> str:
        """
        :return: Email address from which the email was sent.
        """
        return self._from_email

    @property
    def subject(self) -> str:
        """
        :return: Subject of letter.
        """
        return self._subject

    @property
    def send_time(self):
        """
        :return: Datetime when letter sent.
        """
        return self._send_time

    @property
    def letter(self):
        """
        :return: Content of letter.
        """
        return ''

    def __repr__(self):
        return '(Letter name={} from_email={} email={} subject={} send_time={})'.format(self._name, self._from_email,
                                                                                        self._email, self._subject,
                                                                                        self._send_time.strftime('%Y-%m-%d %H:%M:%S'))

    def __hash__(self):
        return hash(self._letter_id)


class Letter(LetterTemplate):
    def __init__(self, to, content, token, session):
        self.domain = 'https://www.emailnator.com'
        self._token = token
        self._s = session
        self._letter = None
        letter_id, _from, subject = content['messageID'], content['from'], content['subject']
        super().__init__(to, *re.findall(r'(.*) <(.*)>', _from)[0], subject, datetime.now(), letter_id)

    @property
    def letter(self):
        if self._letter:
            return self._letter
        payload = json.dumps({'email': self._email, 'messageID': self._letter_id})
        r = self._s.post(f'{self.domain}/message-list', data=payload, headers={**headers, 'x-xsrf-token': self._token})
        if r.status_code == 200:
            self._letter = re.sub(header_regex, '', r.text)
            return self._letter
