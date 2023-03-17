GFaker
=========

Python API Wrapper for `products.aspose.app/email/gmail-generator <https://products.aspose.app/email/gmail-generator>` service and `emailnator.com <https://www.emailnator.com>`

Installation
------------

Usage
-----

Generate gmail address and get emails from it::

    from gfaker import GFaker

    example = GFaker()

    @example.gmailnator.letter_handler()
    def handler(letter):
        print(letter)

    print('fake address:', example.generate_fake_email())
    example.poling()
