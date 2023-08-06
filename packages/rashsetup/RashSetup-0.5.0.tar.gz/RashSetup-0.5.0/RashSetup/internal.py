import sys
import subprocess
import sqlite3
import pathlib
import shutil
import logging
from .crawlers import *

ALL.extend(
    [
        "SettingsParser",
        "ModuleManager"
    ]
)
__all__ = ALL


class SettingsParser:
    def __init__(self, json_url):
        self.parsed = JsonHandler().parse_url(json_url)
        self.url = json_url

    def settings(self):
        return self.url

    def name(self):
        return self.parsed["name"]

    def version(self):
        return self.parsed["version"]

    def hosted(self):
        return self.parsed["hosted"]

    def readme(self):
        return self.parsed.get("readme", False)

    def desc(self):
        return self.parsed.get("desc", "A Rash Module")

    def required(self):
        return self.parsed.get("requires", [])

    def update_readme(self, raw):
        self.parsed["readme"] = raw

    def validate(self):
        required = (
            "name", "version", "hosted"
        )  # required

        return all(
            (
                _ in self.parsed for _ in required
            )
        )

    def install_required(self):
        temp = TempHandler()(False, ".txt")

        with open(temp, 'w') as writer:
            writer.writelines(self.required())

        subprocess.run(
            [
                sys.executable, "-m", "pip", "install", '-r', temp
            ]
        )


class ModulePathManager:
    def __init__(self):
        self.mod = pathlib.Path(__file__).parent / "__RashModules__"
        self.mod.mkdir(exist_ok=True)

        _ = self.mod / "__init__.py"
        None if _.exists() else _.write_text("")

    def check_module(self, name):
        return all(
            (
                (self.mod / name).exists(),
                (self.mod / name / "__init__.py").exists(),
                (self.mod / name / "settings.json").exists()
            )
        )

    def uninstall_module(self, name):
        shutil.rmtree(self.mod / name)

    def gen_path(self, name):
        mod = self.mod / name
        mod.mkdir(exist_ok=True)
        return str(self.mod / name)

    def inquiry(self, module):
        return self.mod / module / "settings.json"


class DBManager(ModulePathManager):
    def __init__(self):
        super().__init__()
        self.sql = self.mod.parent / "__RashSQL__.sql"
        self.connector = sqlite3.connect(self.mod / "__RashModules__.db", check_same_thread=False)

        self.__start()

    def cursor(self):
        return self.connector.cursor()

    def __start(self):
        temp = self.cursor()
        temp.executescript(self.sql.read_text())
        self.connector.commit()

    def sql_code(self, code, *args) -> tuple:
        return self.execute_one_line(
            *self.execute_one_line(
                "SELECT SQL, Empty FROM Sql WHERE Hash = ?", False, code
            ), *args
        )

    def execute_one_line(self, script, all_=False, *args):
        temp = self.cursor()
        temp.execute(script, args)

        return temp.fetchall() if all_ else temp.fetchone()

    def commit(self):
        self.connector.commit()

    def close(self):
        self.connector.close()

    def downloaded(self, name, hosted, version, readme):
        self.sql_code(
            10, name, hosted, version, readme
        )

        self.commit()

    def update_settings(self, name, version, readme=None):
        self.sql_code(
            8, version, name
        )

        self.sql_code(
            9, readme, name
        ) if readme else None

        self.commit()


class HeavyModuleManager(DBManager):
    def fetch_readme(self, url, **_):
        process = Setup(
            READMERawSetup, url
        )

        process.start()
        process.join()

        status, result = process.results()

        if not result:
            logging.exception("Failed to fetch readme from %s.\nDue to %s", url, result)
            return False

        return result

    def investigate(self, url, **_):
        process = Setup(
            SettingsRawSetup, url
        )
        process.start()
        process.join()

        status, result = process.results()

        if not status:
            logging.exception("Failed to fetch settings file from %s.\nDue to %s", url, result)
            return False

        result = SettingsParser(result)

        if not result.validate():
            logging.exception("Invalid settings file")
            return False

        result.update_readme(
            self.fetch_readme(
                result.readme()
            )
        ) if result.readme() else None

        return result

    def download(self, url, path, **_):
        logging.info("Downloading a module from %s", url)

        file = self.investigate(
            url
        )

        if not file:
            return False

        process = Setup(
            RepoRawSetup, url, path
        )

        process.start()
        process.join()

        status, result = process.results()
        if not status:
            return False

        self.update_settings(
            file
        )

        return True

    def check_for_update(self, *args, **_):
        pass

    def update_settings(self, settings: SettingsParser, *_):
        return super().update_settings(
            settings.name(), settings.version(), settings.readme()
        )


class ModuleManager(
    HeavyModuleManager
):
    def __init__(self):
        super().__init__()
        self.linkers = {}

    def activate_link(self, module):
        try:
            if not self.download(
                    self.sql_code(3, module)[0], self.gen_path(module)
            ):
                raise AssertionError("Download Failed")

        except Exception as _:
            logging.exception("Failed to activate %s", module, exc_info=True)
            return False

        else:
            return True

    def activate_all(self):
        logging.info("Checking all modules")

        for module in self.sql_code(5):
            module = module[0]

            if self.check_module(module):
                continue

            result = self.activate_link(module)

            if not (result and self.check_module(module)):
                return False

        return True


class Start:
    def __init__(self):
        manager = ModuleManager()

        root = format_root()
        root.info("Starting RashSetup!")

        if manager.activate_all():
            pass
        else:
            logging.exception("Failed to load default modules :(\nPlease try again!")

        manager.close()

        skip_code = """
import RashSetup.__RashModules__.Rash
RashSetup.__RashModules__.Rash.Start()
"""

        subprocess.run(
            [
                sys.executable,
                "-c",
                skip_code
            ]
        )  # TODO: convert this to Popen and no window as creation flag after preparing exe
