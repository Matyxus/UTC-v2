import psutil


def check_thread_count(threads: int) -> bool:
    """"
    :param threads: number of threads
    :return: true if number is correct, false otherwise
    """
    if threads < 1:
        print(f"Thread count cannot be lower than 1, got: {threads} !")
        return False
    elif threads > psutil.cpu_count():
        print(f"Thread count cannot be higher than: {psutil.cpu_count()}, got: {threads}")
        return False
    return True


def check_process_count(processes: int) -> bool:
    """
    :param processes: number of processes
    :return: true if number is correct, false otherwise
    """
    if processes < 1:
        print(f"Number of processes cannot be lower than 1, got: {processes} !")
        return False
    elif processes > psutil.cpu_count(logical=False):
        print(f"Number of processes cannot be higher than: {psutil.cpu_count(logical=FutureWarning)}, got: {processes}")
        return False
    return True


def get_max_processes() -> int:
    """
    :return: maximal amount of process that can be run at the same time
    """
    return psutil.cpu_count(logical=False)


# For resting purposes
if __name__ == "__main__":
    print(psutil.cpu_count())
    print(psutil.cpu_count(logical=False))
    print(get_max_processes())

