from typing import Dict, List
from datetime import datetime, timedelta

from backup_reader import Backup


class BackupMonitor:
    def __init__(self, backups: Dict[str, List[Backup]], org_list: List[str]) -> None:
        self.backups = backups
        self.all_orgs = org_list
        self.yesterday = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    def find_last_valid_backup(self, backups: List[Backup], org_name: str) -> str:
        sorted_backups = sorted(backups, key=lambda b: b.date, reverse=True)
        for b in sorted_backups:
            if b.date >= self.yesterday:
                continue
            if not b.is_broken_compared_to(backups):
                return f'\u2705 Последняя корректная выгрузка по организации {org_name} - {b.date.date()}.'
        return f"\u26D4 По организации {org_name} нет корректных бэкапов в папке."
    
    def analyze(self) -> List[str]:
        messages = []
        missing = [org for org in self.all_orgs if org not in self.backups]
        for org in missing:
            messages.append(f"\u26D4 По организации {org} не было выгрузки.")
        
        for org, org_backups in self.backups.items():
            found_yesterday = False
            yesterday_broken = False

            for b in org_backups:
                if b.date == self.yesterday:
                    found_yesterday = True
                    if b.is_broken_compared_to(org_backups):
                        yesterday_broken = True
                    break

            if found_yesterday and yesterday_broken:
                message = (f'\u26D4 По организации {org} выгрузка за вчера ({self.yesterday.date()}) битая.'
                            'битая.\n' + self.find_last_valid_backup(org_backups, org))
                messages.append(message)
            elif not found_yesterday:
                message = (f'\u26D4 По организации {org} выгрузки за вчера ({self.yesterday.date()})'
                       ' не было.\n' + self.find_last_valid_backup(org_backups, org))
                messages.append(message)
        return messages