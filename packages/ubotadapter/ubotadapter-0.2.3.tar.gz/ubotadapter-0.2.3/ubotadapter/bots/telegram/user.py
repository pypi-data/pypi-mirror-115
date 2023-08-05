from ubotadapter.user import User


class TelegramUser(User):
    @property
    def data(self) -> dict:
        return super()._data

    def get_visual_name(self) -> str:
        return f'{self.data["first_name"]} {self.data["last_name"]}'

    def get_short_name(self) -> str:
        return self.data["first_name"]

    @property
    def id_url(self) -> str:
        return f'@id{self.data["id"]}'
