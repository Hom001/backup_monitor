import time

from services.backup_reader import BackupReader
from services.backup_monitor import BackupMonitor
from services.notifier import TelegramNotifier
from utils import read_json_list
from core.settings import settings


def main():
    path_to_backups = settings.PATH_TO_BACKUPS
    path_to_org_list = settings.PATH_TO_ORG_LIST

    org_list = read_json_list(path_to_org_list)

    reader = BackupReader(path_to_backups, org_list)
    while True:
        try:
            backups = reader.read_backups()
            break
        except (FileNotFoundError, NotADirectoryError, PermissionError, OSError) as e:
            print(f"Ошибка доступа к папке: {e}")
            print(f"Повтор через 60 секунд...\n")
            time.sleep(60)

    monitor = BackupMonitor(backups, org_list)
    messages = monitor.analyze()

    if not messages:
        messages.append('\u2705 По всем базам выгрузка прошла корректно.')

    notifier = TelegramNotifier()
    notifier.send_messages(messages)


if __name__ == "__main__":
    main()