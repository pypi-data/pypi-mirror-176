import pretty_errors
# from .widgets import timer
from .multiprocess import kill
from .multiprocess import start_server
from .docker import save_all_images as save_docker_images
from .docker import load_dir_images as load_docker_images
from .utils.compress import pack, unpack
from .proxy import clone
from .net import get_ip

func_list = [
    # timer,
    save_docker_images,
    load_docker_images,
    pack,
    unpack,
    start_server,
    kill,
    clone,
    get_ip,
]


def fire_commands():
    import fire
    func_dict = {}
    for func in func_list:
        func_dict[func.__name__] = func
    fire.Fire(func_dict)


def typer_commands():
    import typer
    app = typer.Typer()
    [app.command()(i) for i in func_list]
    app()


def main():
    use_fire = 1
    if use_fire:
        fire_commands()
    else:
        # Fixme *形参 传入会出错，参考这里 https://typer.tiangolo.com/tutorial/multiple-values/arguments-with-multiple-values/
        typer_commands()
