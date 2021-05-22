import pytest

from learning.entities import Todo
from learning.errors import TitleLengthError


def test_create_todo():
    todo = Todo("test todo")

    assert todo.title == "test todo"
    assert not todo.id
    assert not todo.done
    assert not todo.created_at


def test_title_length_is_less_than_0():
    with pytest.raises(TitleLengthError) as exc:
        Todo("")

    assert str(exc.value) == "title length is not between 1 and 256, length: 0"


@pytest.mark.parametrize(
    "title",
    [
        pytest.param("a" * 257, id="single byte"),
        pytest.param("あ" * 257, id="multi byte"),
    ],
)
def test_title_length_is_greater_than_256(title):
    with pytest.raises(TitleLengthError) as exc:
        Todo(title)

    assert str(exc.value) == "title length is not between 1 and 256, length: 257"
