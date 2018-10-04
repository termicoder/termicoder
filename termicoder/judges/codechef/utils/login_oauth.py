import click
import json
from ....utils.logging import logger


def login_oauth():
    home_page = 'http://termicoder.diveshuttam.me/'
    logger.info(
        "Browser window will launch, authorize termicoder with CodeChef.\n"
        "NOTE: If codechef errors about  'Invalid authorization request',\n"
        "Logout of CodeChef and run this command again.\n\n"
        "After authenticating, copy-paste the code returned by the page.")
    click.confirm("Continue?", default=True, abort=True)
    click.launch(home_page)

    # access_token
    strings = []
    logger.info('Paste code from the browser:')
    while(True):
        a = input()
        if a.strip() not in [None, '']:
            strings.append(a)
        else:
            break
    return json.loads('\n'.join(strings))

    # TODO do everything with request-oauthlib
