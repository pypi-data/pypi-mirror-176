import re
import os
import shutil
import tempfile
import subprocess
from pathlib import Path

from cleo.helpers import argument
from cleo.application import Application
from cleo.commands.command import Command
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from typing import Any, List, Dict, Match


class TemplateCommand(Command):

    name = "template"
    description = "Create project from template."
    arguments = [
        argument("repository", "Template repository.", multiple=False),
        argument("directory", "Target directory name.", multiple=False),
    ]

    target_dir: Path
    source_files: List[Path]

    def handle(self) -> Any:
        repository_url = f"ssh://{self.argument('repository')}"
        self.line(f"Clone {repository_url}\n", style="comment")
        self.target_dir = Path(os.getcwd()) / self.argument("directory")
        if self.target_dir.exists() and not self.target_dir.is_dir():
            raise RuntimeError(f"File {self.target_dir} exists.")
        elif self.target_dir.is_dir() and (self.target_dir / "pyproject.toml").exists():
            raise RuntimeError(f"Target directory {self.target_dir} is not empty.")
        tmp_dir = tempfile.mkdtemp()
        try:
            subprocess.check_output(
                ["git", "clone", "--depth=1", repository_url, tmp_dir],
                stderr=subprocess.DEVNULL
            )
            self.run_template_script(
                tmp_dir,
                self.argument("directory")
            )
        finally:
            shutil.rmtree(tmp_dir)

    def c_ignore(self, src: str) -> None:
        source_files = self.source_files[:]
        for exclude in Path(".").glob(str(src)):
            if exclude.is_dir():
                source_files = [p for p in source_files if not p.is_relative_to(exclude)]
            elif exclude in source_files:
                source_files.remove(exclude)
        self.source_files = source_files

    def run_template_script(self, source_dir: str, target: str) -> Any:
        os.chdir(source_dir)
        if not Path("pytemplate.py").exists():
            raise RuntimeError("Script pytemplate.py does not exist.")
        self.source_files = [p for p in Path(".").glob("**/*") if not p.is_relative_to(".git")]
        self.c_ignore("pytemplate.py")
        code_globals = {
            "ignore": self.c_ignore,
            "ask": self.ask,
            "__builtins__": {}
        }
        code_locals = {
            "target": target
        }
        code = Path("pytemplate.py").read_text(encoding="utf-8")
        exec(code, code_globals, code_locals)
        # create directories
        for p in sorted({(p if p.is_dir() else p.parent) for p in self.source_files}):
            os.makedirs(self.target_dir / p, exist_ok=True)
        # copy files
        for p in self.source_files:
            if p.is_dir():
                continue
            if p.name.startswith("@"):
                data = self.apply_context(p.read_text(encoding="utf-8"), code_locals).encode("utf-8")
            else:
                data = p.read_bytes()
            if p.name.startswith("@") or p.name.startswith("#"):
                t = (self.target_dir / p).parent / p.name[1:]
            else:
                t = self.target_dir / p
            t.write_bytes(data)
        os.chdir(self.target_dir)
        self.call("update")
        self.line("\n✨ Done!")

    def apply_context(self, content: str, context: Dict[str, Any]) -> str:
        def repl(m: Match) -> str:
            val = repr(context.get(m.group(1), ""))
            return val[1:-1].replace('"', '\\"') if val.startswith("'") else val[1:-1].replace("'", "\\'")
        return re.sub(r"{%\s*([a-zA-Z_0-9]+)\s*%}", repl, content)


class TemplatePlugin(ApplicationPlugin):
    def activate(self, application: Application, *args: Any, **kwargs: Any) -> None:
        application.command_loader.register_factory("template", TemplateCommand)
