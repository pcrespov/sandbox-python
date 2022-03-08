from typing import NamedTuple

# https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields
# https://docs.python.org/3/library/typing.html#typing.NamedTuple

class Employee(NamedTuple):
    """Represents an employee."""
    name: str
    id: int = 3

    def __repr__(self) -> str:
        return f'<Employee {self.name}, id={self.id}>'


def test_it():
    t = Employee(name="garfield")
    print(t)

    # pylint does not like _asdict!
    #pylint: disable=no-member
    assert t._asdict() == {'id': 3, 'name': 'garfield'}

    print(t._field_types)
    print(t._fields)
    print(t._field_defaults)

    assert t._field_types == {'name': str, 'id':int}    
    assert t._fields == ('name', 'id')
    assert t._field_defaults == {'id': 3}

