# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['state_signals']
install_requires = \
['redis>=3.5,<4.0', 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'state-signals',
    'version': '0.1.0',
    'description': 'Package for easy management of state/event signal publishing, subscribing, and responding',
    'long_description': '# state-signals\nA temporary repo for testing packaging and getting a demo package available\n\nNOTE: License will likely be changed when moved to official repo, just in place here for safety in meantime\n\n# State/Event Signal Module\n\nAdds two new, simple-to-use objects:\n - SignalExporter      (for publishing state signals and handling subscribers + responses)\n - SignalResponder     (for receiving state signals, locking onto publishers, and publishing responses)\n\nAlso provides two dataclass specifications:\n - Signal              (state signal protocol definition)\n - Response            (response protocol definition)\n\nCombining redis pubsub features with state signal + response protocols, \nthese additions make state signal publishing, subscribing, receiving, \nand responding incredibly easy to integrate into any code.\n',
    'author': 'Mustafa Eyceoz',
    'author_email': 'meyceoz@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Maxusmusti/state-signals',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*',
}


setup(**setup_kwargs)
