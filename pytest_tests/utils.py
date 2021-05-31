from learning.entities import Todo


def create_todo(cnt: int):
    return [Todo(title=f"todo no.{i}") for i in range(cnt)]
