import os
import sys
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class BaseLogger(ABC):
    """Abstract base class for the Logger."""

    @staticmethod
    @abstractmethod
    def log(level: str, message: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def error(msg: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def client(msg: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def debug(msg: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def info(msg: str) -> None:
        pass


class Logger(BaseLogger):
    """Concrete implementation of the BaseLogger."""

    log_levels = {
        'INFO': 'INF',
        'DEBUG': 'DBG',
        'ERROR': 'ERR',
        'CLIENT': 'CLT',
        'EXCEPTION': 'EXE'
    }

    @staticmethod
    def _get_current_time() -> str:
        """Returns the current time as a formatted string."""
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def log(level: str, message: str) -> None:
        """Outputs a log message with consistent formatting."""
        prefix = Logger.log_levels.get(level.upper(), 'LOG')
        timestamp = Logger._get_current_time()
        print(f"[{timestamp}] [{prefix}] - {message}")

    @staticmethod
    def error(msg: str) -> None:
        Logger.log("ERROR", msg)

    @staticmethod
    def client(msg: str) -> None:
        Logger.log("CLIENT", msg)

    @staticmethod
    def debug(msg: str) -> None:
        Logger.log("DEBUG", msg)

    @staticmethod
    def info(msg: str) -> None:
        Logger.log("INFO", msg)

    @staticmethod
    def exception(msg: str) -> None:
        Logger.log("EXCEPTION", msg)


def clear_screen() -> None:
    """Clears the console screen (Windows/Linux compatible)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner() -> None:
    """Prints an ASCII banner."""
    print("──────────────────────────────────────────────────────────────")
    print("BEFORE YOU CONTINUE MAKE SURE YOU DO THESE STEPS FIRST")
    print("──────────────────────────────────────────────────────────────")
    print("1. Install Drakensang from the website fully and login one time")
    print("2. Install Drakensang on Steam and launch it, then close it")
    print("3. When thats done, you can click enter to start the script")
    print("──────────────────────────────────────────────────────────────")

    input("Click enter to run the script after you followed the instructions above...")
    print("\n→ Safely migrating your Drakensang Online installation...\n")


def get_user_shortcut_path() -> Path:
    """Automatically resolves the user's Start Menu Drakensang Online shortcut path."""
    user_name = os.getlogin()
    base_path = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    shortcut_path = base_path / "Drakensang Online"

    Logger.debug(f"Detected current user: {user_name}")
    Logger.debug(f"Resolved shortcut path: {shortcut_path}")
    return shortcut_path


class Operation(ABC):
    """Abstract base class for file operations."""

    @abstractmethod
    def execute(self) -> None:
        pass


@dataclass
class CopyOperation(Operation):
    """Recursively copies files and directories from source to destination."""
    src: Path
    dst: Path

    def execute(self) -> None:
        if not self.src.exists():
            Logger.error(f"Source path not found: {self.src}")
            return

        self.dst.mkdir(parents=True, exist_ok=True)

        for root, _, files in os.walk(self.src):
            rel_path = Path(root).relative_to(self.src)
            dest_dir = self.dst / rel_path
            dest_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                src_file = Path(root) / file
                dest_file = dest_dir / file
                try:
                    shutil.copy2(src_file, dest_file)
                except Exception as e:
                    Logger.error(f"Failed to copy '{src_file}': {e}")

        Logger.info("Copy operation completed successfully.")


@dataclass
class DeleteOperation(Operation):
    """Deletes a specified file or folder."""
    target: Path
    recursive: bool = True

    def execute(self) -> None:
        if not self.target.exists():
            Logger.info(f"Target not found, skipping: {self.target}")
            return

        try:
            if self.target.is_dir() and self.recursive:
                shutil.rmtree(self.target)
                Logger.info(f"Deleted directory: {self.target}")
            else:
                self.target.unlink(missing_ok=True)
                Logger.info(f"Deleted file: {self.target}")
        except Exception as e:
            Logger.error(f"Failed to delete '{self.target}': {e}")


@dataclass
class MigrationTask:
    """Represents a named group of migration operations."""
    name: str
    operations: List[Operation] = field(default_factory=list)

    def run(self) -> None:
        Logger.info(f"Starting task: {self.name}")
        for op in self.operations:
            op.execute()
        Logger.info(f"Completed task: {self.name}")


@dataclass
class DrakensangMigrator:
    """Coordinates the migration process."""
    source: Path
    destination: Path
    shortcut: Optional[Path] = None

    def perform_migration(self) -> None:
        """Runs all migration phases with validation."""
        Logger.info("Migration process initiated.")

        if not self.source.exists():
            Logger.error(f"Source directory not found: {self.source}")
            return
        if not self.destination.parent.exists():
            Logger.info(f"Destination parent missing, creating: {self.destination.parent}")
            self.destination.parent.mkdir(parents=True, exist_ok=True)

        tasks = [
            MigrationTask("Copy Game Files", [CopyOperation(self.source, self.destination)]),
            MigrationTask("Delete Shortcut", [DeleteOperation(self.shortcut, recursive=False)]) if self.shortcut else None,
            MigrationTask("Remove Old Installation", [DeleteOperation(self.source, recursive=True)])
        ]

        for task in filter(None, tasks):
            task.run()

        Logger.info("All migration tasks completed successfully.")


def main() -> None:
    """Main entry point for the migration utility."""
    clear_screen()
    print_banner()

    clear_screen()
    print("""
 ____   ___  _____  __  __  ____  ____  ____ 
(  _ \ / __)(  _  )(  \/  )(_  _)(_  _)(_  _)               Author: github.com/Nexriel
 )(_) )\__ \ )(_)(  )    (  _)(_   )(   _)(_                Version: v1.0.1
(____/ (___/(_____)(_/\/\_)(____) (__) (____)
    \n""")

    source = Path(r"C:\Program Files (x86)\Drakensang Online")
    destination = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Drakensang Online")
    shortcut = get_user_shortcut_path()

    migrator = DrakensangMigrator(source, destination, shortcut)

    try:
        migrator.perform_migration()
    except KeyboardInterrupt:
        Logger.exception("Migration aborted by user.")
    except Exception as e:
        Logger.exception(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
