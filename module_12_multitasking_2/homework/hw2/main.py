import subprocess
from shlex import quote


def process_count(username: str) -> int:
    try:
        cmd = f'pgrep -u {quote(username)} | wc -l'
        result = subprocess.run(cmd,
                                shell=True,
                                capture_output=True,
                                text=True,
                                check=True
                                )
        return int(result.stdout.strip())
    except subprocess.CalledProcessError:
        return 0

def total_memory_usage(root_pid: int) -> float:
    # Получаем список всех PID из дерева процессов с корнем root_pid
    pids_cmd = f"pstree -p {root_pid} | grep -o '([0-9]\\+)' | grep -o '[0-9]\\+'"
    pids_result = subprocess.run(pids_cmd, shell=True, capture_output=True, text=True)
    pids = pids_result.stdout.strip().split('\n')

    if not pids or pids == ['']:
        return 0.0

    # Формируем строку с PID через запятую для ps
    pid_list = ",".join(pids)

    # Получаем суммарное потребление памяти (%MEM) для всех PID
    mem_cmd = f"ps -p {pid_list} -o %mem= | awk '{{sum+=$1}} END {{print sum}}'"
    mem_result = subprocess.run(mem_cmd, shell=True, capture_output=True, text=True)

    try:
        return float(mem_result.stdout.strip())
    except ValueError:
        return 0.0


if __name__ == '__main__':
    process_count(username="user")
    root_pid = 1
    total_mem = total_memory_usage(root_pid)
    print(f"Суммарное потребление памяти для дерева процессов с корнем {root_pid}: {total_mem:.2f}%")
