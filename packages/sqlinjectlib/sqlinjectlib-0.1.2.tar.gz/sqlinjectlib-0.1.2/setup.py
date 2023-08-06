# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlinjectlib']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'sqlinjectlib',
    'version': '0.1.2',
    'description': 'A library to simplify SQL injections during CTFs',
    'long_description': '# SQLInjectLib\n\n## Introduction\n\n> A library to simplify SQL injections during CTFs\n\n## Tutorial\n\n> First of all you need to find out the type of injection you need\n>\n> ### Union Injection\n>\n> You need an injection function\n>\n> An injection function is function that takes an SQL expression as input and returns a string\n>\n> #### Example\n>\n> We need to print all the username in a table of users in a website that is vulnerable to a simple union injection\n>\n> The website does something like this in the backend\n>\n> ```php\n> $cursor=query("SELECT name,price FROM cars WHERE name like \'%".$_POST["search"]."%\')\n> foreach($cursor as $elem)\n>   echo $elem[0].",".$elem[1]\n> ```\n>\n> The website gives us the result \'lol\' if we send a string in the search like "42\' union select \'lol\',4"\n>\n> Now we need to build our injection function, the library will use our injection function later to extract informations from the database\n>\n> To do so, we need to:\n>\n> 1. create a string that will be sent to the server\n> 2. send the string to the server\n> 3. parse the response to return the result\n>\n> ```python\n> def injection(expr):\n>     query=f\'42" union select {expr},4\'\n>     response=post(URL,query)\n>     return response.split(\',\')[0]\n> ```\n>\n> in this case our query string is like the example before but with \'lol\' replace with a generic expression\n>\n> post can be anything that sends our query to the server and returns its response\n>\n> We need to return the result of our query, in our case response without the second value (4)\n>\n> Now we need to build our SQLInjector object, in this case we use an UnionInjector object\n>\n> ```python\n> inject = UnionInjector(union_injection, database_type=MySQL())\n> ```\n>\n> This object contains all the code we need to have a nice console to use to perform our injection\n> You need to know the database type, in our example we use MySQL\n>\n> Now to use the object and have our console we use its main method\n>\n> ```python\n> inject.main()\n> ```\n>\n> When you run the program an interactive session will be presented\n>\n> In this console you can execute every SQL query you want plus some special commands\n>\n> With help you can list these special commands\n>\n> _Warning_: if you select a column or a table that does not exist, you could get a python exception and the program may crash\n\n## Installation\n\n> Install locally with:\n>\n> ```bash\n> python3 -m pip install sqlinjectlib\n> ```\n',
    'author': 'rikyiso01',
    'author_email': 'riky.isola@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rikyiso01/sqlinjectlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
