from ward import raises, test

from learning.entities import Todo
from learning.errors import TitleLengthError


@test("create todo")
def _():
    todo = Todo("test todo")

    assert todo.title == "test todo"
    assert not todo.id
    assert not todo.done
    assert not todo.created_at


@test("title length is less than 0")
def _():
    with raises(TitleLengthError) as exc:
        Todo("")

    assert str(exc.raised) == "title length is not between 1 and 256, length: 0"


for title, id in [("a" * 257, "single byte"), ("あ" * 257, "multi byte")]:

    @test(f"title length is greater than 256 [{id}]")
    def _():
        with raises(TitleLengthError) as exc:
            Todo(title)

        assert str(exc.raised) == "title length is not between 1 and 256, length: 257"
