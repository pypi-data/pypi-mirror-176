"""Thanos cleaner"""
import os
import random
import argparse


def get_args() -> argparse.Namespace:
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-target",
        "--target",
        help="path to directory from where files need to be cleaned.",
        required=True,
    )
    return argparser.parse_args()



def find_files(target_dir: str) -> list:
    try:
        file_paths = []
        for root, directories, files in os.walk(target_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
    except PermissionError:
        print("Permission denied. Please provide root Permission.")
    return file_paths


if __name__ == "__main__":
    user_inputs = get_args()
    target_dir = str(user_inputs.target)
    print("Thanos is targeting", target_dir)
    target_files = find_files(target_dir=target_dir)
    print("Targetted Files:")
    for file in target_files:
        print(file)
    random.shuffle(target_files)
    for i in range(0, int(len(target_files) / 2)):
        print("Deleting: ", target_files[i])
        try:
            os.remove(target_files[i])
        except PermissionError:
            print("Root permissoin needed.")
            raise PermissionError
        except Exception:
            pass
    print("Half of them still live!")