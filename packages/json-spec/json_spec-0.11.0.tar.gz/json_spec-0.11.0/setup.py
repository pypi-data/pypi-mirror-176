# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jsonspec',
 'jsonspec.misc',
 'jsonspec.operations',
 'jsonspec.pointer',
 'jsonspec.reference',
 'jsonspec.validators']

package_data = \
{'': ['*'],
 'jsonspec.misc': ['schemas/*', 'schemas/draft-03/*', 'schemas/draft-04/*']}

install_requires = \
['importlib-metadata>=5.0.0,<6.0.0']

extras_require = \
{'cli': ['termcolor']}

entry_points = \
{'console_scripts': ['json = jsonspec.cli:main'],
 'jsonspec.cli.commands': ['add = jsonspec.cli:AddCommand',
                           'check = jsonspec.cli:CheckCommand',
                           'copy = jsonspec.cli:CopyCommand',
                           'extract = jsonspec.cli:ExtractCommand',
                           'move = jsonspec.cli:MoveCommand',
                           'remove = jsonspec.cli:RemoveCommand',
                           'replace = jsonspec.cli:ReplaceCommand',
                           'validate = jsonspec.cli:ValidateCommand'],
 'jsonspec.reference.contributions': ['spec = '
                                      'jsonspec.reference.providers:SpecProvider'],
 'jsonspec.validators.formats': ['css.color = '
                                 'jsonspec.validators.util:validate_css_color',
                                 'email = '
                                 'jsonspec.validators.util:validate_email',
                                 'hostname = '
                                 'jsonspec.validators.util:validate_hostname',
                                 'ipv4 = '
                                 'jsonspec.validators.util:validate_ipv4',
                                 'ipv6 = '
                                 'jsonspec.validators.util:validate_ipv6',
                                 'regex = '
                                 'jsonspec.validators.util:validate_regex',
                                 'rfc3339.datetime = '
                                 'jsonspec.validators.util:validate_rfc3339_datetime',
                                 'uri = jsonspec.validators.util:validate_uri',
                                 'utc.date = '
                                 'jsonspec.validators.util:validate_utc_date',
                                 'utc.datetime = '
                                 'jsonspec.validators.util:validate_utc_datetime',
                                 'utc.millisec = '
                                 'jsonspec.validators.util:validate_utc_millisec',
                                 'utc.time = '
                                 'jsonspec.validators.util:validate_utc_time']}

setup_kwargs = {
    'name': 'json-spec',
    'version': '0.11.0',
    'description': 'Implements JSON Schema, JSON Pointer and JSON Reference.',
    'long_description': 'Json Spec\n=========\n\n.. image:: https://badge.fury.io/py/json-spec.png\n    :target: http://badge.fury.io/py/json-spec\n\n.. image:: https://travis-ci.org/johnnoone/json-spec.png?branch=master\n    :target: https://travis-ci.org/johnnoone/json-spec\n\nThis library implements several JSON specs, like `JSON Schema`_,\n`JSON Reference`_ and `JSON Pointer`_:\n\n* It works on python 3.6 and above\n* It is release under the `BSD license`_\n\n\nInstallation\n------------\n\nThis library has only weak dependencies. You can simply use pip::\n\n    $ pip install json-spec\n\nRegading you needs, you can install more features. For example, this command\nwill enable colorated messages::\n\n    $ pip install json-spec[cli]\n\nThis one will enable ip format for json schema::\n\n    $ pip install json-spec[ip]\n\n...\n\n\nCLI Usage\n---------\n\nThis module expose 2 cli commands.\n\n\n**json-extract** will extract parts of your json document::\n\n    $ json-extract \'#/foo/1\' --document-json=\'{"foo": ["bar", "baz"]}\'\n    $ echo \'{"foo": ["bar", "baz"]}\' | json-extract \'#/foo/1\'\n    $ json-extract \'#/foo/1\' --document-file=doc.json\n    $ json-extract \'#/foo/1\' < doc.json\n\n**json-validate** will validate your document against a schema::\n\n    $ json-validate --schema-file=schema.json --document-json=\'{"foo": ["bar", "baz"]}\'\n    $ echo \'{"foo": ["bar", "baz"]}\' | json-validate --schema-file=schema.json\n    $ json-validate --schema-file=schema.json --document-file=doc.json\n    $ json-validate --schema-file=schema.json < doc.json\n\n\nLibrary usage\n-------------\n\nLet say you want to fetch / validate JSON like objects in you python scripts.\n\nYou can extract member of an object with `JSON Pointer`_::\n\n    from jsonspec.pointer import extract\n\n    obj = {\n        \'foo\': [\'bar\', \'baz\', \'quux\']\n    }\n    assert \'baz\' == extract(obj, \'/foo/1\')\n\n\nYou can resolve member of any object with `JSON Reference`_::\n\n    from jsonspec.reference import resolve\n\n    obj = {\n        \'foo\': [\'bar\', \'baz\', {\n            \'$ref\': \'#/sub\'\n        }],\n        \'sub\': \'quux\'\n    }\n\n    assert \'quux\' == resolve(obj, \'#/foo/2\')\n\n\nYou can describe you data with `JSON Schema`_::\n\n    from jsonspec.validators import load\n\n    # data will validate against this schema\n    validator = load({\n        \'title\': \'Example Schema\',\n        \'type\': \'object\',\n        \'properties\': {\n            \'age\': {\n                \'description\': \'Age in years\',\n                \'minimum\': 0,\n                \'type\': \'integer\'\n            },\n            \'firstName\': {\n                \'type\': \'string\'\n            },\n            \'lastName\': {\n                \'type\': \'string\'\n            }\n        },\n        \'required\': [\n            \'firstName\',\n            \'lastName\'\n        ]\n    })\n\n    # validate this data\n    validator.validate({\n        \'firstName\': \'John\',\n        \'lastName\': \'Noone\',\n        \'age\': 33,\n    })\n\nOther examples can be found in the documentation_ or in the tests_.\n\n.. _`JSON Schema`: http://json-schema.org\n.. _`JSON Reference`: http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03\n.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901\n.. _`BSD license`: https://github.com/johnnoone/json-spec/blob/master/LICENSE\n.. _documentation: http://py.errorist.io/json-spec/\n.. _tests: https://github.com/johnnoone/json-spec/tree/master/tests\n',
    'author': 'Xavier Barbosa',
    'author_email': 'clint.northwood@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://json-spec.readthedocs.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
