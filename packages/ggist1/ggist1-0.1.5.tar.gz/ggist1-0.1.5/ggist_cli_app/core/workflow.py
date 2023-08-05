
import subprocess
import os
from typing import Sequence, Mapping
from dataclasses import dataclass

from ggist_cli_app.core.os import OS


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

        for step in self.steps:
            print(f'running "{step.title}"')
            if self.os in step.cmd:
                flow_cmd = step.cmd[self.os]
            elif OS.any in step.cmd:
                flow_cmd = step.cmd[OS.any]
            else:
                raise LookupError(f'no os config for step {step}')
            print(flow_cmd.cmd)
            os.system(flow_cmd.cmd)
            # subprocess.Popen([step.cmd], stdout=subprocess.PIPE)
