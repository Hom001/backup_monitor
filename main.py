from backup_reader import BackupReader
from backup_monitor import BackupMonitor
from notifier import TelegramNotifier
from utils import read_json_list
import time


def main():
    PATH_TO_BACKUPS = 'Y:'
    PATH_TO_ORG_LIST = r'D:\dev\backup_monitor_v2\data\subd_base.json'

    org_list = read_json_list(PATH_TO_ORG_LIST)

    reader = BackupReader(PATH_TO_BACKUPS, org_list)
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