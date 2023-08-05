import json

from typing import List, Union, Literal


ButtonColors = Literal[
    'primary',  # Обычная
    'secondary',  # "Бледная"
    'positive',  # Зелёная
    'negative',  # Красная
]
ButtonTypes = Literal[
    'text',
    'vkpay',
    'location',
    'callback',
    'open_app',
    'open_link',
]


class Button:
    payload: str
    color: str
    label: str
    type: str

    def __init__(
            self,
            label: str,
            payload: Union[str, dict],
            type: ButtonTypes = 'text',
            color: ButtonColors = 'primary'
    ):
        self.payload = payload
        if isinstance(self.payload, dict):
            self.payload = json.dumps(self.payload, ensure_ascii=False)
        self.color = color
        self.label = label
        self.type = type

    def __str__(self) -> str:
        return json.dumps(self.obj, ensure_ascii=False)

    @property
    def obj(self):
        return {
            'action': {
                'type': self.type,
                'label': self.label,
                'payload': self.payload
            },
            'color': self.color
        }


class Keyboard:
    buttons: List[List[Button]]
    one_time: bool
    inline: bool

    def __init__(
            self,
            buttons: Union[Button, List[Button], List[List[Button]]] = None,
            inline: bool = True,
            one_time: bool = False
    ):
        self.buttons = []
        if buttons is not None:
            self.add_buttons(buttons)
        if inline and one_time:
            raise ValueError(
                'inline и one_time -- взаимоисключающие параметры'
            )
        self.inline = inline
        self.one_time = one_time

    def __str__(self) -> str:
        return self.jsonize()

    def add_buttons(self, buttons: Union[Button, List[Button]]):
        # TODO: возможность использовать описание кнопки вместо объекта
        if isinstance(buttons, Button):
            buttons = [buttons]
        self.buttons.append(buttons)

    def jsonize(self, alt_buttons: List[List[Button]] = None) -> str:
        # XXX: зачем здесь аргумент alt_buttons?
        if alt_buttons is None:
            alt_buttons = self.buttons
        return json.dumps({
            'one_time': self.one_time,
            'inline': self.inline,
            'buttons': [[b.obj for b in li] for li in alt_buttons]
        }, ensure_ascii=False)

    def format_label(self, data: Union[tuple, dict]) -> 'Keyboard':
        # XXX: это должно быть в кнопках
        for line in self.buttons:
            for button in line:
                try:
                    button.label = button.label % data
                except TypeError:
                    pass
        return self

    def format_payload(self, data: Union[tuple, dict]) -> 'Keyboard':
        # XXX: это должно быть в кнопках
        for line in self.buttons:
            for button in line:
                try:
                    button.payload = button.payload % data
                except TypeError:
                    pass
        return self
