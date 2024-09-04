import os
import subprocess
import argparse
from typing import List, Union 


executed_commands = set()
test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test", "test_main.py")
files_to_exclude = map(os.path.abspath, [__file__, test_path])

def get_sorted_files(directory) -> List[str]:
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file[-3:] == ".py":
                file_paths.append(os.path.join(root, file))    
    return sorted(file_paths)

def cmds_first_step_check(file_path: str) -> bool:
    with open(file_path, "r") as file:
        for line in file:
            if "CMDS" in line:
                return True
    return False


def get_cmds(file_path: str) -> Union[List[str], None]:
    local_vars = {}
    with open(file_path, "r") as file:
        try:
            exec(file.read(), {}, local_vars)
        except:
            pass
    cmds = local_vars.get("CMDS", [])
    return cmds


def extract_cmds_from_file(file_path: str) -> Union[List[str], None]:
    cmds = get_cmds(file_path)
    return cmds


def execute_commands_from_file(file_path: str) -> None:
    cmds = []
    if cmds_first_step_check(file_path):
        cmds = extract_cmds_from_file(file_path)

    if cmds:
        for cmd in cmds:
            if "echo" in cmd:
                if cmd not in executed_commands:
                    try:
                        subprocess.run(cmd, shell=True, check=True)
                        executed_commands.add(cmd)
                    except subprocess.CalledProcessError as e:
                        print(f"не удалось выплонить '{cmd}' из {file_path}: {e}")
                else:
                    print(f'команда "{cmd}" уже выполнялась')


def find_and_execute_commands(root_dir: str) -> None:
    for file_path in get_sorted_files(root_dir):
        if os.path.abspath(file_path) not in files_to_exclude:
            execute_commands_from_file(file_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Скрипт парсит все скрипты в указанной директории и исполняет их \
        в сортированном порядке пропуская повторяющиеся команды"
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Путь до директории со скриптами. Если не указан, то будет использована \
            текущая директория",
    )
    args = parser.parse_args()
    script_dir = args.path if args.path else "./"
    if os.path.isdir(script_dir):
        find_and_execute_commands(script_dir)
    else:
        raise FileNotFoundError(f"Путь '{script_dir}' не найден")


if __name__ == "__main__":
    main()
