def get_file_name(experiment_name: str, extension="png"):
    import os
    from pathlib import Path

    sim_directory = Path(__file__).resolve().parent

    files = list(
        filter(
            lambda f: experiment_name in f,
            os.listdir(os.path.join(sim_directory, "results")),
        )
    )

    nth_result = _get_next_number(files)

    return os.path.join(
        sim_directory,
        "results",
        experiment_name.strip("__") + f"__{nth_result}.{extension}",
    )


def _get_next_number(files: list[str], delimiter="__") -> int:
    last = 0
    for f in files:
        last = max(last, int(f.split(".")[0].split(delimiter)[-1]))
    return last + 1
