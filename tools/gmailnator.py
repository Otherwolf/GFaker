import json
from typing import List
from urllib.parse import unquote

from .exceptions import ProblemWithGetEmail, CloudflareDetect
from .mail.letter import Letter
from .mail import Mail


headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'content-type': 'application/json'
}


class GmailNator(Mail):
    """
    Class for work with https://www.emailnator.com
    """

    def __init__(self, proxy=None):
        super().__init__(proxy)
        self.domain = 'https://www.emailnator.com'
        r = self._s.get(self.domain)
        if r.status_code == 403:
            raise CloudflareDetect()

    def __get_xsrf_token(self) -> str:
        token = self._s.cookies.get('XSRF-TOKEN', '')
        if not token:
            raise CloudflareDetect()
        return unquote(token)

    def get_email(self) -> str:
        return self.set_email(self.get_email_online())

    def get_email_online(self, use_custom_domain=True, use_plus=True, use_point=True) -> str:
        """
        Random email address from the site.

        :param use_custom_domain: Generate email not only from @gmail.com.
        :param use_plus: Generate email with "+" in address.
        :param use_point:  Generate email with "." in address.
        :return: Random email address.
        """
        data = ['domain', 'plusGmail', 'dotGmail']
        payload = json.dumps({'email': [i for i, k in zip(data, [use_custom_domain, use_plus, use_point]) if k]})
        r = self._s.post(f'{self.domain}/generate-email',
                         headers={**headers, 'x-xsrf-token': self.__get_xsrf_token()}, data=payload)
        if r.status_code == 200:
            return str(self._set_email(r.json()['email'][0]))
        raise ProblemWithGetEmail()

    def set_email(self, email: str) -> str:
        """
        Make sure you use the email address associated with this site, or it won't work
        """
        return self._set_email(email)

    def get_inbox(self) -> List[Letter]:
        payload = json.dumps({'email': self._email})
        r = self._s.post(f'{self.domain}/message-list',
                         headers={**headers, 'x-xsrf-token': self.__get_xsrf_token()}, data=payload)
        if r.status_code == 200:
            return [Letter(self._email, _letter, self.__get_xsrf_token(), self._s) for _letter in r.json()['messageData'] if
                    'ADS' not in _letter['messageID']]
        return []

    def is_empty_handlers(self):
        return not self._handlers


if __name__ == '__main__':
    gen = GmailNator()
    email = gen.get_email_online(False, True, False)
    print(email)

    gen.poling(4)
