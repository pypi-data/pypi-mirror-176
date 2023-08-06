from pathlib import Path
from importlib import import_module
from typing import Optional

from modulepy import log
from modulepy.Base import Base, Information


class Loader(object):
    @staticmethod
    def load_module(module_path: Path, debug: bool = True) -> Optional[Base]:
        if not module_path.is_file() or not module_path.suffix == ".py":
            return None
        try:
            cwd = Path(".").absolute().__str__()
            if module_path.__str__().startswith(cwd):
                import_path = module_path.__str__().replace(cwd, "")[1:].replace("/", ".").replace(".py", "")
                module_name = module_path.name[:-3]
                log.info(f"Attempting to load module '{module_name}' from '{import_path}'.")
                return getattr(import_module(import_path, module_name), module_name)
            else:
                log.error(f"'{module_path}' is not in '{cwd}'")
        except Exception as e:
            log.error(f"Could not load module: {module_path}")
            if debug:
                log.exception(e)
            return None

    @staticmethod
    def load_modules(module_directory_path: Path) -> list[Base]:
        r = []
        if not module_directory_path.is_dir():
            return r
        for module_path in module_directory_path.glob("*.py"):
            m = Loader.load_module(module_path)
            if m is not None:
                r.append(m)
        return r

    @staticmethod
    def contains_module(module_directory: Path, info: Information, ignore_version: bool = False) -> bool:
        def matcher(module: Base) -> bool:
            return module.information.name == info.name and \
                   (ignore_version or module.information.version == info.version)
        return any([matcher(m) for m in Loader.load_modules(module_directory)])
