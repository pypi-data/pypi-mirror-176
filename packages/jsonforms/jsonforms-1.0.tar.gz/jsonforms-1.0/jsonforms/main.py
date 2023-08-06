from dataclasses import dataclass
from asyncio import get_event_loop

@dataclass
class Key:
    name: str
    required: bool = True
    value: str = ''
    valid: bool = False

class JSONForm:
    def __init__(self, *args: Key) -> None:
        self.__args = {key.name: key for key in args}
    
    @property
    def args(self) -> dict[str, Key]:
        return self.__args

    @property
    def keys(self) -> tuple[str]:
        return tuple(key for key in self.__args.keys())

    @property
    def values(self) -> tuple[str]:
        return tuple(keyobject.value for keyobject in self.__args.values())

    @property
    def valid_values(self) -> tuple[bool]:
        return tuple(keyobject.valid for keyobject in self.__args.values())

    def set_valid(self, *, key: str) -> None:
        self.__args[key].valid = True

    def is_required(self, *, key: str) -> bool:
        return self.__args[key].required

class JSONFormChecker:
    async def aiocheck(self, *, json: dict, form: JSONForm):
        IS_VALID = False

        for key, value in form.args.items():
            value: Key

            if (current := json.get(value.name, None)) and (current is not None and current != ''):
                form.set_valid(key=key)
                IS_VALID = True
                continue

            elif form.is_required(key=key) is False:
                form.set_valid(key=key)
                IS_VALID = True
                continue

            else:
                IS_VALID = False
                break

        if False in form.valid_values: IS_VALID = False

        return IS_VALID

    def check(self, *, json: dict, form: JSONForm):
        loop = get_event_loop()
        return loop.run_until_complete(self.aiocheck(json=json, form=form))