
from typing import Sequence, Mapping, Optional
from dataclasses import dataclass
from rich.console import Console

from ggist_cli_app.core.os import OS
from subprocess import PIPE, run

@dataclass(frozen=True)
class WorkflowCommand:
    cmd: str

@dataclass(frozen=True)
class WorkflowStep:
    title: str
    description: str
    cmd: Mapping[OS, WorkflowCommand]

class Workflow:

    def __init__(self, steps: Sequence[WorkflowStep], os: OS):
        self.steps = steps
        self.os = os

    
    def play(self):
        console = Console()
        error_console = Console(stderr=True, style="bold red")

        

        def out(command):
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result

        for ii, cmd in enumerate(self.commands):
            
            console.print(f'[bold]running step {ii+1} out of {len(self.steps)}: "{cmd.cmd}"\n')

            r = out(cmd.cmd)
            
            console.print(r.stdout)
            console.print(r.stderr)

            if r.returncode:
                error_console.print("failed to run step")
                return

            # subprocess.Popen([step.cmd], stdout=subprocess.PIPE)
            # console.log(f"step {ii+1} complete")
            
                
        console.print("[bold green]Flow completed")
    
    @property
    def commands(self)->Optional[list[WorkflowCommand]]:
        commands = []
        console = Console()
        error_console = Console(stderr=True, style="bold red")
        for ii, step in enumerate(self.steps):
            if self.os in step.cmd:
                commands.append(step.cmd[self.os])
            elif OS.any in step.cmd:
                commands.append(step.cmd[OS.any])
            else:
                error_console.print(f'step #{ii}({step.title}) missing your operating system support ({self.os})')
                return None
        return commands
