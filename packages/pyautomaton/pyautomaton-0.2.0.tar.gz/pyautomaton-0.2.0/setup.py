# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyautomaton']

package_data = \
{'': ['*'], 'pyautomaton': ['pyfsm.egg-info/*']}

setup_kwargs = {
    'name': 'pyautomaton',
    'version': '0.2.0',
    'description': '',
    'long_description': '# PyAutomaton\n\n## Description \nPyAutomaton is a simple library implementing Mealy state machines, thus meaning that the events produced by the automaton are determined by the tuple (state, event) and not only on the current state, as happens with Moore state machines. \n\n## Usage\nPyAutomaton offers the possibility of declare State Machines by using a fluent descriptive style.\nFor example, given the state machine in the following figure: \n![turntile-picture](docs/imgs/turntile.png)\n\nthe code implementing this state machine is: \n```python\nfsm = Automaton().start_from("locked").go_in("locked").when("push") \\\n                    .coming_from("locked").go_in("unlocked").when("coin") \\\n                    .coming_from("unlocked").go_in("unlocked").when("coin") \\\n                    .coming_from("unlocked").go_in("locked").when("push")\n```\n\nAnd the machine can run by invoking the fsm object as follow: \n```python\nfsm(\'push\')\n```\neach invocation triggers a state transition and returns the corresponding action, if any.',
    'author': 'cirius1792',
    'author_email': 'cirolucio.tecce@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
