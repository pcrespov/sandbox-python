
from helpers import some_func_using_Foo


def test_mock_class_member(mocker):
    mocker.patch("helpers.Foo.bar", return_value=77)

    assert some_func_using_Foo() == 77