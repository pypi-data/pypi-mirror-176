import click
from ggist_cli_app.commands.groups import play
from ggist_cli_app.context import click_pass_context
from ggist_cli_app.core.workflow import WorkflowStep, Workflow
from ggist_cli_app.core.os import OS
from ggist_cli_app.core.workflow import WorkflowCommand
import inquirer
from rich.console import Console

FLOWS = {
    'k8s-setup': Workflow([
        WorkflowStep(title='Say Hello', description='', cmd={OS.any: WorkflowCommand("echo 'hello'")}),
        WorkflowStep(title='Download the latest release with the command', description='', cmd={
            OS.linux: WorkflowCommand("""curl -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\""""),
            OS.osx: WorkflowCommand("""curl -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\""""),
        }),
        WorkflowStep(title='Validate the binary', description='', cmd={
            OS.linux: WorkflowCommand("""curl -LO \"https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256\""""),
            OS.osx: WorkflowCommand("""curl -LO \"https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256\""""),
        }),
        WorkflowStep(title='Validate Sha', description='', cmd={
            OS.linux: WorkflowCommand("""echo \"$(cat kubectl.sha256)  kubectl\" | sha256sum --check"""),
            OS.osx: WorkflowCommand("""echo \"$(cat kubectl.sha256)  kubectl\" | sha256sum --check"""),
        }),
        WorkflowStep(title='Install in the system', description='', cmd={
            OS.linux: WorkflowCommand("""sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl"""),
            OS.osx: WorkflowCommand("""sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl"""),
        }),
        WorkflowStep(title='Test', description='', cmd={
            OS.any: WorkflowCommand("""kubectl version --client"""),
        }),
        WorkflowStep(title='Cleanup', description='', cmd={
            OS.linux: WorkflowCommand("""rm -rf kubectl kubectl.sha256"""),
            OS.osx: WorkflowCommand("""rm -rf kubectl kubectl.sha256"""),
        }),
    ], None),
    'awscli-setup': Workflow([ # https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
        WorkflowStep(title='Download the pkg installer', description='', cmd={
            OS.osx: WorkflowCommand("""curl \"https://awscli.amazonaws.com/AWSCLIV2.pkg\" -o \"AWSCLIV2.pkg\""""),
            OS.linux: WorkflowCommand("""curl \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"awscliv2.zip\""""),
        }),
        WorkflowStep(title='Run the pkg installer', description='', cmd={
            OS.osx: WorkflowCommand("""sudo installer -pkg AWSCLIV2.pkg -target /"""),
            OS.linux: WorkflowCommand("""unzip awscliv2.zip && sudo ./aws/install"""),
        }),
        WorkflowStep(title='Validation', description='', cmd={
            OS.osx: WorkflowCommand("""aws --version"""),
            OS.linux: WorkflowCommand("""aws --version"""),
        }),
        WorkflowStep(title='Configure', description='', cmd={
            OS.osx: WorkflowCommand("""aws configure"""),
            OS.linux: WorkflowCommand("""aws configure"""),
        }),
    ], None),

}
@play.command()
@click.argument('flow_name',  required=False)
@click_pass_context
def flow(context, flow_name: str):
    """
    Play a workflow
    """
    if not flow_name:
        questions = [
            inquirer.List(
                "flow",
                message="What flow to run",
                choices=tuple(FLOWS.keys()),
            ),
        ]

        answers = inquirer.prompt(questions)
        flow_name = answers['flow']

    console = Console()
    error_console = Console(stderr=True, style="bold red")

    if flow_name in FLOWS:
        wf = FLOWS[flow_name]
        wf.os = context.os

        if not wf.commands:
            error_console.print('This flow is not supported by your os') 
            return 

        console.print(f'This will execute {len(wf.commands)} shell commands:')
        for command in wf.commands:
            console.print(f'[gray] - {command.cmd}')
        
        questions = [
            inquirer.Confirm("sure", message="Continue?", default=True)]

        answers = inquirer.prompt(questions)

        if answers['sure']:     
            wf.play()
        else:
            console.print("[bold red]Skipped. you answered 'NO'")
    else:
        error_console.print('I don\'t know this flow')        
