# CleanChausie

CleanChausie is a data validation and transformation library for Python. It is a successor to CleanCat.

*Interested in working on projects like this? [`Close`](https://close.com) is looking for [great engineers](https://jobs.close.com) to join our team.*

Key features:

- Operate on/with type-checked objects that have good IDE/autocomplete support
- Annotation-based declarations for simple fields
- Composable/reusable fields and field validation logic
- Support (but not require) passing around a context (to avoid global state)
  - Context pattern is compatible with explicit sqlalchemy-based session management. i.e. pass in a session when validating
- Cleanly support intra-schema field dependencies (i.e. one field can depend on the validated value of another)
- Explicit nullability/omission parameters
- Errors returned for multiple fields at a time, with field attribution

## Installation

CleanChausie requires Python 3.8+.
To install, run `python3 -m pip install cleanchausie`.

## CleanChausie by example

### A basic example in Flask

This shows:

- Annotation-based declarations for simple fields.
- Type-checked objects (successful validation results in initialized instances of the schema)

```python
from typing import List
from cleanchausie.fields import (
    EmailField, ListField, URLField, ValidationError, field
)
from cleanchausie.schema import Schema
from flask import app, request, jsonify

class JobApplication(Schema):
    first_name: str
    last_name: str
    email: str = field(EmailField())
    urls: List[str] = field(ListField(URLField(default_scheme='http://')))

@app.route('/job_application', methods=['POST'])
def test_view():
    result = JobApplication.clean(request.json)
    if isinstance(result, ValidationError):
        return jsonify({'errors': [{'msg': e.msg, 'field': e.field} for e in result.errors] }), 400

    # Now "result" has the validated data, in the form of a `JobApplication` instance.
    assert isinstance(result, JobApplication)
    name = f'{result.first_name} {result.last_name}'
```

### Explicit nullability

TODO: revisit omission defaults so that they match the annotation

```python
from typing import Optional, Union
from cleanchausie.consts import OMITTED
from cleanchausie.fields import field, StrField, Omittable, Required
from cleanchausie.schema import Schema

class NullabilityExample(Schema):
    # auto defined based on annotations
    nonnull_required: str
    nullable_omittable: Optional[str]

    # manually specified
    nonnull_omittable: Union[str, OMITTED] = field(StrField(), nullability=Omittable(allow_none=False))
    nullable_required: Optional[str] = field(StrField(), nullability=Required(allow_none=True))
```

### Composable/reusable fields

```python
from typing import Union
from cleanchausie.fields import field, Field, StrField, IntField, Error
from cleanchausie.schema import Schema

@field(parents=(StrField(),))
def trimmed_string(value: str) -> str:
    return value.strip()

def max_val(max_value: int) -> Field:
    @field()
    def _max_val(value: int) -> Union[int, Error]:
        if value > max_value:
            return Error(msg=f'value is above allowed max of {max_value}')
        return value
    return _max_val

def min_val(min_value: int) -> Field:
    @field()
    def _min_val(value: int) -> Union[int, Error]:
        if value < min_value:
            return Error(msg=f'value is below allowed min of {min_value}')
        return value
    return _min_val

def constrained_int(min: int, max: int) -> Field:
    return field(parents=(IntField(), min_val(min), max_val(max)))

class ReusableFieldsExampleSchema(Schema):
    first_name: str = trimmed_string
    age: int = field(parents=(IntField(), min_val(0)))
    score: int = constrained_int(min=0, max=100)
```

### Context support

```python
import attrs
from cleanchausie.fields import field, StrField
from cleanchausie.schema import Schema

class MyModel:  # some ORM model
    id: str
    created_by: 'User'

@attrs.frozen
class Context:
    authenticated_user: 'User'  # the User making a request
    session: 'Session'  # active ORM Session

class ContextExampleSchema(Schema):
    @field(parents=(StrField(),), accepts=('id',))
    def obj(self, value: str, context: Context) -> MyModel:
        return (
            context.session
            .query(MyModel)
            .filter(MyModel.created_by == context.authenticated_user.id)
            .filter(MyModel.id == value)
        )

with atomic() as session:
    result = ContextExampleSchema.clean(
        data={'id': 'mymodel_primarykey'},
        context=Context(authenticated_user=EXAMPLE_USER, session=session)
    )
assert isinstance(result, ContextExampleSchema)
assert isinstance(result.obj, MyModel)
```

### Intra-schema field dependencies

```python
from cleanchausie.fields import field
from cleanchausie.schema import Schema

class DependencyExampleSchema(Schema):
    a: str
    b: str
    
    @field()
    def a_and_b(self, a: str, b: str) -> str:
        return f'{a}::{b}'


result = DependencyExampleSchema.clean(
    data={'a': 'foo', 'b': 'bar'},
)
assert isinstance(result, DependencyExampleSchema)
assert result.a_and_b == 'foo::bar'
```

### Per-field errors

```python
from cleanchausie.fields import (
    Error, ValidationError, field
)
from cleanchausie.schema import Schema

class PerFieldErrorExampleSchema(Schema):
    first_name: str
    last_name: str

result = PerFieldErrorExampleSchema.clean({})
assert isinstance(result, ValidationError)
assert result.errors == [
    Error(msg='This field is required.', field=('last_name',)),
    Error(msg='This field is required.', field=('first_name',))
]
```

## Release process

- Make sure to thoroughly review and test the code changes.
- Make sure you have [`releaserabbit`](https://github.com/closeio/releaserabbit) installed.
- From the project's root run `releaserabbit` with the desired version increment - `major`, `minor` or `patch`.
- A version bump should happen automatically, and the new version should be uploaded to PyPI.
