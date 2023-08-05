# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['typeapi']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.0.0']

setup_kwargs = {
    'name': 'typeapi',
    'version': '1.1.0',
    'description': '',
    'long_description': '# typeapi\n\n[![Python](https://github.com/NiklasRosenstein/python-typeapi/actions/workflows/python.yml/badge.svg)](https://github.com/NiklasRosenstein/python-typeapi/actions/workflows/python.yml)\n\n__Compatibility__: Python 3.6.3+\n\nThe `typeapi` package provides an object-oriented interface for introspecting type hints from the `typing` and\n`typing_extensions` module at runtime. Currently, only a subset of the different kinds of type hints are supported,\nnamely through the following representations:\n\n| Concrete type | Description |\n| ------------- | ----------- |\n| `ClassTypeHint` | For any normal or generic type as well as `typing.Any`. Provides access to the underlying type, the type arguments and parameters, if any. |\n| `UnionTypeHint` | Represents `Union` type hint and gives access to the union members. |\n| `LiteralTypeHint` | Represents a `Literal` type hint and gives access to the literal values. |\n| `AnnotatedTypeHint` | Represents an `Annotated` type hint and gives access to the annotated type as well as the metadata. |\n| `TypeVarTypeHint` | Represents a `TypeVar` type hint and gives an interface to access the variable\'s metadata (such as constarints, variance, ...). |\n| `ForwardRefTypeHint` | Represents a forward reference. |\n\nThe main entry point to wrapping a low-level type hint is the `TypeHint()` constructor.\n\n## Examples\n\nInspect a `List[int]` type hint:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import ClassTypeHint, TypeHint\nfrom typing import List\n\nhint = TypeHint(List[int])\nassert isinstance(hint, ClassTypeHint)\nassert hint.type is list\n\nitem_hint = hint[0]\nassert isinstance(item_hint, ClassTypeHint)\nassert item_hint.type is int\n```\n\nRetrieve the metadata from an `Annotated[...]` type hint:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import AnnotatedTypeHint, ClassTypeHint, TypeHint\nfrom typing_extensions import Annotated\n\nhint = TypeHint(Annotated[int, 42])\nassert isinstance(hint, AnnotatedTypeHint)\nassert hint.type is int\nassert hint.metadata == (42,)\n\nsub_hint = hint[0]\nassert isinstance(sub_hint, ClassTypeHint)\nassert sub_hint.type is int\n```\n\nParameterize one type hint with the parameterization of a generic alias:\n\n```py\n# cat <<EOF | python -\nfrom dataclasses import dataclass\nfrom typeapi import ClassTypeHint, TypeHint\nfrom typing import Generic, TypeVar\nfrom typing_extensions import Annotated\n\nT = TypeVar("T")\n\n@dataclass\nclass MyGeneric(Generic[T]):\n  value: T\n\nhint = TypeHint(MyGeneric[int])\nassert isinstance(hint, ClassTypeHint)\nassert hint.get_parameter_map() == {T: int}\n\nmember_hint = TypeHint(T).parameterize(hint.get_parameter_map())\nassert isinstance(member_hint, ClassTypeHint)\nassert member_hint.type is int\n```\n\nEvaluate forward references:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import ClassTypeHint, ForwardRefTypeHint, TypeHint\nfrom typing import List\n\nMyVector = List["MyType"]\n\nclass MyType:\n  pass\n\nhint = TypeHint(MyVector)\nassert isinstance(hint, ClassTypeHint)\nassert hint.type is list\n\nitem_hint = hint[0]\nassert isinstance(item_hint, ForwardRefTypeHint)\nassert item_hint.expr == "MyType"\n\nhint = hint.evaluate(globals())\nitem_hint = hint[1]\nassert isinstance(item_hint, ClassTypeHint)\nassert item_hint.type is MyType\n```\n\n## Planned work\n\n* Support more features of the typing system (e.g. `ClassVar`, `ParamSpec`, ...)\n* Support evaluating forward references that utilize newer Python language features (such as built-in type subscripts\n  and type union syntax).\n    * Subscript support could be achieved by mocking the built-in types during the evaluation of the expression.\n    * Type unions could be achieved by rewriting the expression AST before evaluating and mocking every value in the expression.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
