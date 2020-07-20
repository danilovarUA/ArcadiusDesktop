LANGUAGES = ["en", "de", "ru", "emoji"]

translation = {
    # Please put new words in alphabetic order 🥺
    "accounts": ['Accounts', 'Accounts', 'Аккаунты', '🔐'],
    "add_accounts": ['Add Accounts', '???', 'Добавить аккаунты', '🆕'],
    "attack": ['Attack', 'Angriff', 'Атака', '⚔️'],
    "attacks": ['Attacks', 'Angriffe', 'Атаки', '🔫'],
    "bot": ['Bot', 'Bot', 'Бот', '🤖'],
    "change_password": ['Change Password', '???', 'Изменить пароль', '🔏'],
    "defense": ['Defense', 'Verteidigung', 'Оборона', '🛡'],
    "economy": ['Economy', 'Wirtschaft', 'Экономика', '💰'],
    "email": ['Email', 'Email', 'Email', '📧'],
    "error": ['Error', 'Fehler', 'Ошибка', '😱'],
    "forum": ['Forum', 'Forum', 'Форум', '🗣'],
    "id": ['id', 'id', 'id', '???'],
    "interface": ['Interface', 'Anzeige', 'Интерфейс', '🙂'],
    "license": ['License', 'Lizenz', 'Лицензия', '📄'],
    "load_servers": ['Load Servers', '???', 'Загрузить сервера', '🤓'],
    "logs": ['Logs', 'Verlauf', 'Логи', '📚'],
    "mail": ['Email', 'Email', 'Email', '📧'],
    "messages": ['Messages', 'Nachrichten', 'Сообщения', '📩'],
    "module": ['Module', 'Modul', 'Модуль', '😳'],
    "name": ['Name', 'Name', 'Имя', '😇'],
    "other": ['Other', 'Sonstiges', 'Другие', '👻'],
    "overview": ['Overview', 'Übersicht', 'Обзор', '👀'],
    "password": ['Password', '???', 'Пароль', '🔑'],
    "points": ['Points', 'Punkte', 'Очки', '🔢'],
    "remove_accounts": ['Remove Accounts', '???', 'Удалить аккаунт', '🚷'],
    "reports": ['Reports', 'Berichte', 'Доклады', '📈'],
    "seconds": ['Seconds', 'Sekunden', 'Секунд', '⏳'],
    "server": ['Server', 'Server', 'Сервер', '🌎'],
    "settings": ['Settings', 'Einstellungen', 'Настройки', '⚙️'],
    "text": ['Text', 'Text', 'Текст', '🔤'],
    "time": ['Time', 'Zeitstempel', 'Время', '⏳'],
    "tools": ['Tools', 'Werkzeuge', 'Инструменты', '🛠'],

    "language_multi": ["Language/???/Язык/👅"] * len(LANGUAGES),

    "tab_accounts_no_servers_selected_popup_text": ["Servers not selected",
                                                    "???",
                                                    "Не выбраны сервера",
                                                    "???"],
    "wrong_credentials_popup": ["Wrong email or password",
                                "???",
                                "Не верный email или пароль",
                                "???"],
    "language_warning": ["WARNING: Changing the Language will restart the whole GUI.",
                         "WARNUNG: Das ändern der Sprache wird die GUI neustarten.",
                         "Внимание: Изменение языка перезапустит весь интерфейс.",
                         "🤬🤬🤬"],
    "minimum_time_between_requests": ["Minimum time between requests in seconds",
                                      "Minimale Wartezeit zwischen einzelnen Anfragen",
                                      "Минимальное время между запросами",
                                      "🤯🤯🤯"],

}


class Translation:
    def __init__(self, perm_dict):
        # TODO: create a script that sets up all the default values if they are not in there
        self.language = perm_dict["settings"]["language"]

    def get_text(self, key):
        try:
            language_index = LANGUAGES.index(self.language)
        except ValueError:
            raise ValueError("{} - wrong language".format(self.language))
        return translation[key][language_index]
