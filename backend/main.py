from src.infra.app import create_app
from src.utils.lint import run_lint
from injector import Injector


run_lint()

app = create_app(injector=Injector())
