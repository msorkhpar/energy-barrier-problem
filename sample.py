from multiprocessing import Lock, Process, Queue, current_process
import time
import queue  # imported for using queue.Empty exception


class data:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def do_job(tasks_to_accomplish):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
            time.sleep(int(task.id))
            print(task)
        except queue.Empty:
            break


def main():
    number_of_task = 20
    number_of_processes = 10
    tasks_to_accomplish = Queue()
    processes = []

    for i in range(number_of_task):
        tasks_to_accomplish.put(data(i, f"Task {i}"))

    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
