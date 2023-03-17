import random
import string
from typing import Optional

import requests
from requests_toolbelt import MultipartEncoder

from .exceptions import ProblemWithGetEmail


class Aspose:
    def __init__(self, email_with_inbox: str):
        """
        :param email_with_inbox: gmail address that we will contain real messages
        """
        self.domain = 'https://api.products.aspose.app'
        self.email_with_inbox = email_with_inbox

    def generate_fake_gmail(self) -> Optional[str]:
        """
        create fake gmail
        :return:
        """
        m = MultipartEncoder(fields={'email': self.email_with_inbox}, boundary=self._generate_boundary())
        headers = {"Content-Type": m.content_type}
        target_url = f'{self.domain}/email/api/FakeEmail/Generate'
        response = requests.post(target_url, headers=headers, data=m)
        if response.status_code < 300:
            return response.json().get('GeneratedAddress')
        raise ProblemWithGetEmail()

    @staticmethod
    def _generate_boundary() -> str:
        """
        generate content type for .NET
        :return:
        """
        boundary = '----WebKitFormBoundary' \
                   + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        return boundary


if __name__ == '__main__':
    a = Aspose('fakegmail@gmail.com')
    assert isinstance(a.generate_fake_gmail(), str)
