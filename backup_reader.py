from typing import List, Dict, Tuple
from datetime import datetime
import re
import os


class Backup:
    def __init__(self, filename: str, size_kb: int, date_str: str) -> None:
        self.filename = filename
        self.size_kb = size_kb
        self.date = datetime.strptime(date_str, "%d-%m-%Y")

    def is_broken_compared_to(self, others: List['Backup']) -> bool:
        for other in others:
            if other is not self and self.size_kb < (other.size_kb // 2):
                return True
        return False
        
    def __repr__(self):
        return f"{self.filename} ({self.date.date()}, {self.size_kb} KB)"
    

class BackupReader:
    def __init__(self, path: str, active_databases: List[str]) -> None:
        self.path = path
        self.active_databases = active_databases

    def parse_filename(self, filename: str) -> Tuple[str, str]:
        pattern = r"_(?=\d)"
        parts = re.split(pattern, filename, maxsplit=1)
        date = parts[1].split('.')[0]
        return parts[0], date
    
    def read_backups(self) -> Dict[str, List[Backup]]:
        result = {}
        for filename in os.listdir(self.path):
            org_name, date = self.parse_filename(filename)
            if org_name not in self.active_databases:
                continue
            full_path = os.path.join(self.path, filename)
            size_kb = os.path.getsize(full_path) // 1024
            backup = Backup(filename, size_kb, date)
            result.setdefault(org_name, []).append(backup)
        return result