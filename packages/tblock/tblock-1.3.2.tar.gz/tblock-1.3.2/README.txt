TBLOCK

An anti-capitalist ad-blocker that uses the hosts file

SUMMARY

-   About
-   Features
-   Installation
-   Post-installation
-   Usage
-   Issues
-   Copyright
-   Libraries used
-   Contact

ABOUT

TBlock is a free and open-source ad-blocker, written in Python. It uses
the hosts file to block advertising and tracking domains, which means it
protects your whole system against these domains. TBlock is compatible
with most of filter formats, and also has a built-in filter converter,
to help you share your custom filters with people that are using
different ad-blockers.

FEATURES

-   Free and open-source software
-   Easy to install
-   Does not cost any money
-   Does not track your personal data
-   Does not make you fingerprintable, unlike some ad-blocking browser
    extensions
-   Fast rules parsing
-   Blocks ads for your whole operating system
-   Compatible with most filter formats
-   Has an online filter repository to help you find and subscribe to
    filters in an easier way
-   Has a built-in filter converter

INSTALLATION

There are various methods to install TBlock. You need to install TBlock
as root, since superuser privileges are required to edit the hosts file.

With python

This is the fastest and easiest way to install TBlock on your machine.
Simply run the following command:

    $ sudo pip install tblock

Other installation methods

More installation methods can be found on our website:

Manually

To build TBlock manually, see BUILDING.md.

POST-INSTALLATION

After the installation and after each update of TBlock, you should
update your local version of the remote filter repository and subscribe
to a blocking filter, by running:

    $ sudo tblock -Sy tblock-base

USAGE

To show the help page of TBlock, simply run:

    $ tblock -h

To show the help page of the built-in converter, simply run:

    $ tblockc -h

You can find more help about usage on TBlock’s wiki.

ISSUES

If you found an issue or that you want to request a new feature, you
have multiple options (because we don’t want to force our users to join
Codeberg to contribute to the project): - Open an issue on Codeberg -
Contact us via Email - Contact us on Matrix - Contact us on XMPP -
Contact us on Mastodon

LICENSE

TBlock, its converter and its logo are released under GPLv3.

LIBRARIES USED

TBlock uses the external libraries:

  Name       Author             License      Homepage
  ---------- ------------------ ------------ -------------------------------------
  colorama   Jonathan Hartley   BSD          https://github.com/tartley/colorama
  requests   Kenneth Reitz      Apache 2.0   https://requests.readthedocs.io
  urllib3    Andrey Petrov      MIT          https://urllib3.readthedocs.io/

CONTACT

-   Email: tblock@e.email [PGP key]
-   Mastodon: @tblock@fosstodon.org
-   Telegram: https://t.me/tblock
-   Website: https://tblock.codeberg.page/
