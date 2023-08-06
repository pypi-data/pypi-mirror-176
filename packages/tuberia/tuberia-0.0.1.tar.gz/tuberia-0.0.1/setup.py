# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src', 'pytest_tuberia': 'src/pytest_tuberia'}

packages = \
['pytest_tuberia', 'tuberia']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'loguru>=0.6.0,<0.7.0',
 'makefun>=1.14.0,<2.0.0',
 'prefect>=1.2.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

extras_require = \
{'pyspark': ['pyspark==3.3.0', 'delta-spark==2.1.0']}

entry_points = \
{'console_scripts': ['tuberia = tuberia.__main__:main'],
 'pytest11': ['pytest_tuberia = pytest_tuberia']}

setup_kwargs = {
    'name': 'tuberia',
    'version': '0.0.1',
    'description': 'Tuberia... when data engineering meets software engineering',
    'long_description': '<p align="center">\n    <a href="https://aidictive.github.io/tuberia" target="_blank">\n        <img src="https://aidictive.github.io/tuberia/images/logo.png"\n             alt="Tuberia logo"\n             width="800">\n    </a>\n</p>\n<p align="center">\n    <a href="https://github.com/AIdictive/tuberia/actions/workflows/cicd.yaml" target="_blank">\n        <img src="https://github.com/aidictive/tuberia/actions/workflows/cicd.yaml/badge.svg"\n             alt="Tuberia CI pipeline status">\n    </a>\n    <a href="https://app.codecov.io/gh/AIdictive/tuberia/" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/aidictive/tuberia"\n             alt="Tuberia coverage status">\n    </a>\n    <a href="https://github.com/AIdictive/tuberia/issues" target="_blank">\n        <img src="https://img.shields.io/bitbucket/issues/AIdictive/tuberia"\n             alt="Tuberia issues">\n    </a>\n    <a href="https://github.com/aidictive/tuberia/graphs/contributors" target="_blank">\n        <img src="https://img.shields.io/github/contributors/AIdictive/tuberia"\n             alt="Tuberia contributors">\n    </a>\n    <a href="https://pypi.org/project/tuberia/" target="_blank">\n        <img src="https://pepy.tech/badge/tuberia"\n             alt="Tuberia total downloads">\n    </a>\n    <a href="https://pypi.org/project/tuberia/" target="_blank">\n        <img src="https://pepy.tech/badge/tuberia/month"\n             alt="Tuberia downloads per month">\n    </a>\n    <br />\n    Data engineering meets software engineering\n</p>\n\n---\n\n:books: **Documentation**:\n<a href="https://aidictive.github.io/tuberia" target="_blank">\n    https://aidictive.github.io/tuberia\n</a>\n\n:keyboard: **Source Code**:\n<a href="https://github.com/aidictive/tuberia" target="_blank">\n    https://github.com/aidictive/tuberia\n</a>\n\n---\n\n\n## 🤔 What is this?\n\nTuberia is born from the need to bring the worlds of data and software\nengineering closer together. Here is a list of common problems in data\nprojects:\n\n* Loooooong SQL queries impossible to understand/test.\n* A lot of duplicate code due to the difficulty of reusing it in SQL queries.\n* Lack of tests, sometimes because the used framework does not facilitate\ntesting tasks.\n* Lack of documentation.\n* Discrepancies between the existing documentation and the latest deployed code.\n* A set of notebooks deployed under the Databricks Share folder.\n* A generic notebook with utility functions.\n* Use of drag-and-drop frameworks that limit the developer\'s creativity.\n* Months of intense work to migrate existing pipelines from one orchestrator to\nanother (e.g. from Airflow to Prefect, from Databricks Jobs to Data\nFactory...).\n\nTuberia aims to solve all these problems and many others. \n\n\n## 🤓 How it works?\n\nYou can view Tuberia as if it were a compiler. Instead of compiling a\nprogramming language, it compiles the steps necessary for your data pipeline to\nrun successfully.\n\nTuberia is not an orchestrator, but it allows you to run the code you write in\nPython in any existing orchestrator: Airflow, Prefect, Databricks Jobs, Data\nFactory....\n\nTuberia provides some abstraction of where the code is executed, but defines\nvery well what are the necessary steps to execute it. For example, this shows\nhow to create a PySpark DataFrame from the `range` function and creates a Delta\ntable.\n\n```python\nimport pyspark.sql.functions as F\n\nfrom tuberia import PySparkTable, run\n\n\nclass Range(PySparkTable):\n    """Table with numbers from 1 to `n`.\n\n    Attribute:\n        n: Max number in table.\n\n    """\n    n: int = 10\n\n    def df(self):\n        return self.spark.range(self.n).withColumn("id", F.col(self.schema.id)\n\n\nclass DoubleRange(PySparkTable):\n    range: Range = Range()\n\n    def df(self):\n        return self.range.read().withColumn("id", F.col("id") * 2)\n\n\nrun(DoubleRange())\n```\n\n!!! warning\n\n    Previous code may not work yet and it can change. Please, notice this\n    project is in an early stage of its development.\n\nAll docstrings included in the code will be used to generate documentation\nabout your data pipeline. That information, together with the result of data\nexpectations/data quality rules will help you to always have complete and up to\ndate documentation.\n\nBesides that, as you have seen, Tuberia is pure Python so doing unit tests/data\ntests is very easy. Programming gurus will enjoy data engineering again!\n',
    'author': 'guiferviz',
    'author_email': 'guiferviz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aidictive/tuberia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
