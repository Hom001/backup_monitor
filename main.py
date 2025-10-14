from backup_reader import BackupReader
from backup_monitor import BackupMonitor
from notifier import TelegramNotifier
from utils import read_json


def main():
    PATH_TO_BACKUPS = 'Y:'
    PATH_TO_ORG_LIST = r'D:\dev\backup_monitor_v2\data\subd_base.json'

    org_list = read_json(PATH_TO_ORG_LIST)

    reader = BackupReader(PATH_TO_BACKUPS, org_list)
    backups = reader.read_backups()

    monitor = BackupMonitor(backups, org_list)
    messages = monitor.analyze()

    notifier = TelegramNotifier()
    notifier.send_messages(messages)


if __name__ == "__main__":
    main()