import psutil
from subprocess import Popen, PIPE, check_output
import os



def print_table(table):
    header = ["PID", "PROC", "CWD", "MEM(Mb)"]
    if len(table) > 0:
        table[0] = header
    else:
        print("there is no java process")
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    print('\n')
    for line in table:
        print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")


def get_result():

    resultTable = []

    jps_folder = os.path.dirname(os.path.realpath(Popen(['which', 'java'], stdout=PIPE).communicate()[0].strip()))
    if 'jdk' not in jps_folder:
        jps_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(Popen(['which', 'java'], stdout=PIPE).communicate()[0].strip())))) + '/bin'

    jps_path = jps_folder + "/jps"
    if os.path.isfile(jps_path): 
        jps_processes = check_output([jps_path]).split("\n")
    else:
        raise Exception("there is no jps in your machine")

    for process in jps_processes:
        process_pid = process.split(" ")[0]
        try: 
            int(process_pid)
            if psutil.pid_exists(int(process_pid)):
                p = psutil.Process(int(process_pid))
                resultTable.append([str(p.pid),process.split()[1], str(p.cwd()),str(round(p.memory_info()[0] / 1000000))])
            else:
                pass
        except:
            pass
    return resultTable


def ram_sum(result_list):
    ram_sum = 0
    for l in result_list:
        ram_sum += float(l[3])
    print('--'*5)
    print("Total memory usage (Mb): %.2f \n" %(ram_sum))


def main():
    print_table(get_result())
    ram_sum(get_result())


if __name__ == '__main__':
    main()
