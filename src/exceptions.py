from shutil import ExecError


class ConvertToPdfException(Exception):
    """Вызывается при ошибке конверсии прайсов."""
    pass


class TelegramSendDocumentException(Exception):
    """Вызывается при ошибке отправки прайса в Telegram."""
    pass


class TelegramSendMessageExeption(ExecError):
    """Вызывается при ошибке отправки сообщения в Telegram."""
    pass
