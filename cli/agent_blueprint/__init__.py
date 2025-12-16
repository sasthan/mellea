import typer
import os
import shutil

agent_blueprint_app = typer.Typer(name="agent_blueprint", help="Create a new Mellea Agent using the Agent Blueprint.")

@agent_blueprint_app.command("init")
def init_agent(name: str = typer.Option(..., help="Name of the new agent")):
    base_dir = os.path.join(os.getcwd(), name)

    if os.path.exists(base_dir):
        typer.echo(f"Directory '{name}' already exists. Aborting.")
        raise typer.Exit()

    os.makedirs(base_dir)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, "templates")

    for file_name in ["main.py", "double_round_robin.py", "test_agent.py", "README.md"]:
        src = os.path.join(templates_dir, file_name)
        dst = os.path.join(base_dir, file_name)
        if os.path.exists(src):
            shutil.copy(src, dst)

    typer.echo(f" Minimal Mellea agent '{name}' created at: {base_dir}")
    typer.echo("You can now run the agent with:")
    typer.echo(f"python {os.path.join(name, 'main.py')} \"your question\"")
    typer.echo("And test the agent with:")
    typer.echo(f"python {os.path.join(name, 'test_agent.py')}")