# starter download Python Packages
#   * pandas from python packages
#   * openpyxl form python packages
#   * pip install tksheet from terminal
#   * pip install pyinstaller form terminal

import pandas as pd                                                                        # import library pandas
from tkinter import *                                                                      # import library tkinter
from tkinter import filedialog                                                             # import command filedialog

# function import file excel {before process}
def openFile():
    filepath = filedialog.askopenfilename()
    return filepath                                                                        # return select path file

button = Button(text="Open",command=openFile)
button.pack()                                                                              # create GUI button

excel_file = openFile()                                                                    # file excel name test
df = pd.read_excel(excel_file)                                                             # set read mode file excel

# df.at[0,'Burst Time']
# df.loc[i,'Process':'Priority']
# df.loc[i,['Process','Priority']]

# set parameter in global
global arr_p,burst,start,stop, burst_all, loop_data, avg_wait, avg_turn_a, Throughput, cpu_utilization
loop_data = 20

# create data type array  { a:all, p:process, f:finish, t:time, output:show }
data_a = []
data_p = []
data_f = []
data_t = []
data_output = []
# Create Table Using Tkinter
class Table:
    def __init__(self, root):
        for i in range(total_rows):                                      # set max row table =  i
            for j in range(total_columns):                               # set max columns table = j
                self.e = Entry(root, width=20, fg='black',               # set page width and color font
                               font=('Salome', 16 ))                     # set font and size font
                self.e.grid(row=i, column=j)                             # set grid row, columns
                self.e.insert(END, data_output[i][j])                    # insert data in table {data_output}

#  function first process
def first_process():
    # set parameter
    arr_p = 0
    stop_1 = 0
    start_1 = 0
    burst = 0
    # set for loop input data 0 -> first burst time process {input data || arrival time = 0}
    for i in range(0,df.at[0, 'Burst Time'],1):
        data_p.append(df.loc[i, 'Process':'Priority'])                         # input data at data_p array
        arr_p +=1                                                              # arrival time + 1
        stop_1 +=1                                                             # stop process + 1
        burst += 1                                                             # burst time + 1
    turn_a = stop_1 - data_p[0][2]                                             # turn around = stop - arrival time
    wait_t = turn_a - data_p[0][1]                                             # waiting time = turn around - burst time
    data_f.append(data_p[0])                                                   # input data at data_f array
    data_t.append([start_1, stop_1, turn_a, wait_t])                           # input time at data_t array
    pop(0)                                                                     # remove process finish form data_p

    return arr_p ,stop_1 , burst                                               # return time to main function

# function calculate burst time
# select data array {1:data_p, 2:data_a, 3:data_f}
def cal_burst(check):
    burst_process=0
    if(check == 1):
        for i in range(0, len(data_p), 1):                                   # for loop 0 - len array {data_p}
            burst_process += data_p[i][1]                                    # burst time += burst time
        return burst_process                                                 # return burst time to main function
    elif(check == 2):
        for i in range(0, len(data_a), 1):                                   # for loop 0 - len array {data_a}
            burst_process += data_a[i][1]
        return burst_process
    elif (check == 3):
        for i in range(0, len(data_f), 1):                                   # for loop 0 - len array {data_f}
            burst_process += data_f[i][1]
        return burst_process

# function calculate time
def cal_time():
    Average_Waiting = 0
    Average_Turnaround = 0
    for i in range(0,len(data_t),1):
        Average_Waiting += data_t[i][3]                                    # all_waiting += waiting time from data_t
        Average_Turnaround += data_t[i][2]                                 # all_turn_A  += turn around  from data_t
    Average_Waiting /= len(data_t)                                         # avr_wait = all_waiting / num process
    Average_Turnaround /= len(data_t)                                      # avr_turn_A = all_turn_A / num process
    cpu_utilization = (cal_burst(3))/cal_burst(3)*100       # cpu = |all_time process - null|/all_time process * 100
    Throughput = len(data_t)/cal_burst(3)                                  # Throughput = num process/all time process
    return round(Average_Turnaround,3), round(Average_Waiting,3), round(Throughput,3), round(cpu_utilization,3)

# function add data array {data_a} | data-excel to data-array
def add_all_data():
    loop = 0
    while (loop <= 19):                                                # while loop 0-19
        data_a.append(df.loc[loop, 'Process':'Priority'])              # input data form data_a info (Process->Priority)
        loop += 1

# function remove data in array
# select index
def pop(i):
    if (not isEmpty()):                                               # if in array have data can delete data
        lastElement = data_p[i]                                       # set parameter data_[i] i:index
        del (data_p[i])                                               # command delete
        return lastElement                                            # return information
    else:
        return ("Stack Already Empty")                                # if in array haven't data can show text

# function link between pop and inEmpty {isEmpty check have or haven't data in array}
def isEmpty():
    return data_p == []

# function process algorithm non-preemptive priority
# function type in-out data
def process(arr_p,stop,burst):
    start = stop                                                     # set time start = stop
    loop = 0
    burst_p = data_p[0][1]                                           # set burst_process = data index [0][1]
    if(arr_p+burst_p > 19):                                          # if arrival time + burst time > 19
        max = 19                                                     # data excel max arrival time
        start_p = arr_p                                              # start = arrival time
        loop_p = max - start_p                                       # max-arrival time - arrival time process
        for i in range(0,loop_p,1):
            data_p.append(df.loc[start_p + i, 'Process':'Priority'])    # add data from data_p {Process->Priority}
            data_p.sort(key=lambda i: i[3])                             # sort data in array {sort Priority}
        burst += burst_p                                                # burst time = burst time + burst time process
        arr_p = max                                                     # set arrival time = max arrival time
        stop = start + data_p[0][1]                                # stop = start + burst time first process {data_p}
        turn_a = stop - data_p[0][2]                                      # turn around time = stop - arrival time
        wait_t = turn_a - data_p[0][1]                                    # waiting time = turn_A - burst time
        data_f.append(data_p[0])                                          # input process finish to data_f
        data_t.append([start, stop, turn_a, wait_t])                      # input time process finish to data_t
        pop(0)                                                            # remove process finish form data_p
        return arr_p, stop, burst                                         # return arrival time, stop and burst time
    else:
        while (loop < burst_p):
            data_p.append(df.loc[arr_p + loop, 'Process':'Priority'])
            data_p.sort(key=lambda i: i[3])
            arr_p += 1
            loop += 1
        burst += burst_p
        stop = start + data_p[0][1]
        turn_a = stop - data_p[0][2]
        wait_t = turn_a - data_p[0][1]
        data_f.append(data_p[0])
        data_t.append([start, stop, turn_a, wait_t])
        pop(0)
        return arr_p, stop, burst

# save parameter data to data_a and calculate burst time all_data
add_all_data()
burst_all = cal_burst(2)

# start first process and output data function to main {arrival time, stop and burst process}
arr_p, stop, burst = first_process()

# second process by finish all process and input-output data function to main {arrival time, stop and burst process}
while(len(data_p) != 0):                                                # stop process if array data_p == null
    arr_p, stop , burst = process(arr_p, stop,burst)

# output data timer by function cal_time  {average waiting time, average turn around, Throughput and CPU time}
avg_turn_a,avg_wait,Throughput, cpu_utilization = cal_time()

# add topic output process first array {data_output}
data_output.append(['Process','Priority','Start','Stop','Turn Around Time', 'Waiting Time'])
for i in range(0,len(data_f),1):
    # data [ Process  ,  Priority  , start  ,  stop  ,  Turn around time  ,  waiting time ]
    data_output.append([data_f[i][0],data_f[i][3],data_t[i][0],data_t[i][1],data_t[i][2],data_t[i][3]])

# show data time
print(f"CPU utilization: {cpu_utilization} %")
print(f"Throughput: {Throughput} ")
print(f"Average Turnaround time: {avg_turn_a} ")
print(f"Average Waiting time : {avg_wait} ")
total_rows = len(data_output)                                    # set parameter maximum row table
total_columns = len(data_output[0])                              # set parameter maximum column table

root = Tk()
t = Table(root)
root.mainloop()