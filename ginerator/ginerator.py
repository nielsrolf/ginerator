import os
from pathlib import Path
import click
import importlib.util


def command_with_ginfile(base_command, filepath):
    save_dir = filepath.split("/")[-1][:-4]
    filepath = os.path.abspath(filepath)
    return (base_command + \
        f"    --save_dir=\"$RESULTS_DIR/{save_dir}\" \\\n"
        f"    --gin_file={filepath} \n\n")


def combine_all(options):
    if isinstance(options, str):
        yield [options]
        return
    if isinstance(options, list):
        for value in options:
            for expanded in combine_all(value):
                yield expanded
        return
    options = dict(**options)
    keys = list(options.keys())
    head = keys[0]
    # if the current key is a gin file, include that
    if head.endswith(".gin"):
        first_include = [head]
    else:
        first_include = []
    # if there is only one key in the dict, iterate over its val
    if len(keys) == 1:
        for  val in combine_all(options[head]):
            yield first_include + val
        return
    # there is a tail and we combine each combination for
    # head with each combination for tail
    tail = keys[1:]
    for head_val in combine_all(options.pop(head)):
        for tail_val in combine_all(options):
            yield first_include + head_val + tail_val


@click.command()
@click.argument('config_file')
def generate_configs(config_file):
    spec = importlib.util.spec_from_file_location("ginerator.options", config_file)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    commands = []
    os.makedirs(Path(config.filename_prefix + "_").parent.absolute(), exist_ok=True)

    gin_include = "include '{}'\n".format
    for combination in combine_all(config.options):
        filename = config.filename_prefix + "_".join([i.split("/")[-1][:-4] for i in combination]) + ".gin"
        commands += [command_with_ginfile(config.base_command, filename)]

        with open(filename, "w") as f:
            for include_file in combination:
                f.write(gin_include(include_file))

    with open(config.commands_file, "w") as f:
        for cmd in commands:
            f.writelines(cmd)
