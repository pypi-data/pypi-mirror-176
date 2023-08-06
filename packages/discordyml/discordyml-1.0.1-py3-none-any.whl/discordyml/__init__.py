from re import *
from ast import *
from abc import *
from collections.abc import *


class Item(ABC):
    """Anything which has a snowflake `.id`, e.g. Guild, Channel, User"""

    id: int


def get_raw(user_id: int):
    """return (user data, full data)"""
    with open("discord.yml", "a+") as f:
        f.seek(0)
        data = f.read()
    try:
        return search(f"(?ms){user_id}:\n.*?(?=\n(?! )|\Z)", data).group(), data
    except AttributeError:
        return None, data


class Vars:
    """Example: ```
    db = Vars()
    author = ctx.author
    db[author, "foo"] = 12
    print(db[author, "foo"]) # 12
    del db[author, "foo"]
    try:
        db[author, "foo"]
    except Exception as e:
        print(e) # User Example#0000 has no variable named foo
        ```"""

    def __getitem__(self, var: (Item, str)):
        try:
            string = search(
                f"(?s)(?<={escape(var[1])}: ).+?(?=\n.*?: |\Z)", get_raw(var[0].id)[0]
            ).group()
        except:
            raise KeyError(f"{var[0]} has no variable named {var[1]}")
        array = string.split("\n - ")
        return (
            literal_eval(array[0])
            if len(array) == 1
            else list(map(literal_eval, array))
        )

    def __setitem__(self, var: (Item, str), value):
        item = var[0].id
        split = "\n - "
        item_raw, data = get_raw(item)
        with open("discord.yml", "w") as f:
            f.write(
                sub(
                    f"(?m)^{item}:\n|\Z",
                    rf"{item}:\n {var[1]}:"
                    rf" {split+split.join(value)if isinstance(value,Sequence)else value!r}",
                    data.replace(
                        item_raw,
                        sub(f"(?ms) {escape(var[1])}: .+(?=^.*: |\Z)", "", item_raw),
                    )
                    if item_raw
                    else data,
                    1,
                )
            )

    def __delitem__(self, var: (Item, str)):
        item_raw, data = get_raw(var[0].id)
        with open("discord.yml", "w") as f:
            f.write(
                data.replace(
                    item_raw,
                    sub(f"(?ms) {escape(var[1])}: .+(?=^.*: |\Z)", "", item_raw),
                )
            )
