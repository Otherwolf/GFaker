from tools.aspose import Aspose
from tools.gmailnator import GmailNator


class GFaker:
    """
    API Wrapper for service which provides temporary email address
    """

    def __init__(self):
        self.gmailnator = GmailNator()
        self._root_email = self.gmailnator.get_email_online(True, True, True)
        self.aspose = Aspose(self._root_email)

    def __repr__(self):
        return u'<GFaker [{0}]>'.format(self._root_email)

    def generate_fake_email(self):
        return self.aspose.generate_fake_gmail()

    def poling(self, timeout: int = 5):
        self.gmailnator.poling(timeout)


if __name__ == '__main__':
    example = GFaker()

    @example.gmailnator.letter_handler()
    def handler(letter):
        print(letter)

    print('email:', example.generate_fake_email())
    example.poling()
