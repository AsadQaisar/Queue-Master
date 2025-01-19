import heapq

import numpy as np
import csv
from tkinter import filedialog
from scipy.stats import *
import pandas as pd
from xlsxwriter import Workbook
import openpyxl
from openpyxl.chart import BarChart, Reference
import os


# FOR QUEUING MODEL
# M/M/C
def mmc_queue(lambd, mu, c):
    lmbd = 1 / lambd
    mue = 1 / mu
    rho = lmbd / (mue * c)
    p0 = 1 - rho

    Lq = round((rho ** 2) / (1 - rho), 3)
    Wq = round((Lq / lmbd), 3)
    Ws = round((Wq + 1 / mue), 3)
    Ls = round((lmbd * Ws), 3)
    utilization = round((rho), 3)
    idle = p0
    return Lq, Wq, Ws, Ls, utilization, idle


# M/G/C
def mgc_queue(lambd, c, general_distribution, min_mean_shape, max_var_scale):
    lmbd = 1 / lambd

    if general_distribution == "Normal Distribution":
        mue = 1 / min_mean_shape
        var = max_var_scale
        rho = lmbd / (mue * c)
        lq = (((lmbd ** 2) * var) + rho ** 2)
        Lq = round(lq / (2 * (1 - rho)), 3)

    elif general_distribution == "Uniform Distribution":
        mu = (min_mean_shape + max_var_scale) / 2
        mue = 1 / mu
        rho = lmbd / (mue * c)
        var_sq = ((max_var_scale - min_mean_shape) ** 2) / 12
        lq = (((lmbd ** 2) * var_sq) + rho ** 2)
        Lq = round(lq / (2 * (1 - rho)), 3)

    elif general_distribution == "Gamma Distribution":
        mu = min_mean_shape * max_var_scale
        mue = 1 / mu
        rho = lmbd / (mue * c)
        var_g = min_mean_shape * (max_var_scale ** 2)
        lq = (((lmbd ** 2) * var_g) + rho ** 2)
        Lq = round(lq / (2 * (1 - rho)), 3)
        # Lq = round((rho ** 2) * (min_mean_shape * (max_var_scale ** 2) + 1) / (2 * (1 - rho)), 3)

    else:
        raise ValueError("Invalid service distribution")

    Wq = round((Lq / lmbd), 3)
    Ws = round((Wq + (1 / mue)), 3)
    Ls = round((lmbd * Ws), 3)
    utilization = round((rho), 3)

    return Lq, Wq, Ws, Ls, utilization


# G/G/C
def ggc_queue(arrival_distribution, service_distribution, min_mean_shape_arvl, min_mean_shape_srvc, max_var_scale_arvl,
              max_var_scale_srvc, c):
    # Arrival (Lambda)
    global lmbd, rho, Ca, Cs
    if arrival_distribution == "Normal Distribution":
        lmbd = 1 / min_mean_shape_arvl
        var_a = max_var_scale_arvl
        Ca = var_a / ((1 / lmbd) ** 2)

    elif arrival_distribution == "Uniform Distribution":
        lambd = (min_mean_shape_arvl + max_var_scale_arvl) / 2
        lmbd = 1 / lambd
        var_sq_a = ((max_var_scale_arvl - min_mean_shape_arvl) ** 2) / 12
        Ca = var_sq_a / ((1 / lmbd) ** 2)

    elif arrival_distribution == "Gamma Distribution":
        lambd = min_mean_shape_arvl * max_var_scale_arvl
        lmbd = 1 / lambd
        var_sqr_a = min_mean_shape_arvl * (max_var_scale_arvl ** 2)
        Ca = var_sqr_a / ((1 / lmbd) ** 2)

    else:
        raise ValueError("Invalid service distribution")

    # Service (mu)
    if service_distribution == "Normal Distribution":
        mue = 1 / min_mean_shape_srvc
        var_s = max_var_scale_srvc
        rho = lmbd / (mue * c)
        Cs = var_s / ((1 / mue) ** 2)

    elif service_distribution == "Uniform Distribution":
        mu = (min_mean_shape_srvc + max_var_scale_srvc) / 2
        mue = 1 / mu
        var_sq_s = ((max_var_scale_srvc - min_mean_shape_srvc) ** 2) / 12
        rho = lmbd / (mue * c)
        Cs = var_sq_s / ((1 / mue) ** 2)

    elif service_distribution == "Gamma Distribution":
        mu = min_mean_shape_srvc * max_var_scale_srvc
        mue = 1 / mu
        var_sqr_s = min_mean_shape_srvc * (max_var_scale_srvc ** 2)
        Cs = var_sqr_s / ((1 / lmbd) ** 2)

    else:
        raise ValueError("Invalid service distribution")

    lq = ((rho ** 2) * (1 + Cs)) * (Ca + ((rho ** 2) * Cs))
    Lq = round((lq / (2 * (1 - rho) * (1 + ((rho ** 2) * Cs)))), 3)
    Wq = round((Lq / lmbd), 3)
    Ws = round((Wq + (1 / mue)), 3)
    Ls = round((lmbd * Ws), 3)
    utilization = round((rho), 3)

    return Lq, Wq, Ws, Ls, utilization


'''
Lq, Wq, Ws, Ls, utilization = ggc_queue("Normal Distribution", "Normal Distribution", 10, 8, 20, 25, 1)
print (Lq, Wq, Ws, Ls, utilization)
'''


# FOR SIMULATION

# SAVE SIMULATION RESULT IN EXCEL FILE FUNCTION
def save_excel(filename, rand, inter_arrival, arrival, service, priority_values,
               completion, waiting_time, turnaround_time, response_time,
               inter_arrival_mean, arrival_mean, service_mean,
               avg_waiting_time, avg_turnaround_time, avg_response_time):
    # Create a Pandas Excel writer using xlsxwriter
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        # Save the simulation results to the Excel file
        data = {'S.no.': np.arange(rand),
                'Inter Arrival': inter_arrival,
                'Arrival': arrival,
                'Service': service,
                'Priority': priority_values,
                'Completion': completion,
                'Turnaround Time': turnaround_time,
                'Waiting Time': waiting_time,
                'Response Time': response_time}

        df = pd.DataFrame(data)

        df.to_excel(writer, sheet_name='Results', startrow=1, header=False, index=False)

        workbook = writer.book
        worksheet = writer.sheets['Results']

        # Set a header format
        header_format = workbook.add_format({'bold': True, 'fg_color': 'yellow'})

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Write the means
        means_data = [['Means:', inter_arrival_mean, arrival_mean, service_mean, 'N/A',
                       'N/A', avg_turnaround_time, avg_waiting_time, avg_response_time]]

        for i, row in enumerate(means_data):
            for j, value in enumerate(row):
                worksheet.write(i + len(df) + 2, j, value, header_format)  # Adjust the row accordingly

        # Add Gantt chart
        gantt_chart = workbook.add_chart({'type': 'bar'})

        # Assuming 'Arrival' column for the x-axis and 'Completion' column for the duration
        gantt_chart.add_series({
            'name': 'Gantt Chart',
            'categories': f'=Results!$C$2:$C${rand + 1}',  # Adjust accordingly
            'values': f'=Results!$F$2:$F${rand + 1}',  # Adjust accordingly
        })

        # Set axis labels
        gantt_chart.set_x_axis({'name': 'Completion Time'})
        gantt_chart.set_y_axis({'name': 'Arrival Time'})

        # Insert the chart into the worksheet
        worksheet.insert_chart('H2', gantt_chart)  # Adjust the position accordingly

    # Open the saved Excel file
    os.startfile(filename)


# PRIORITY FUNCTION
def generate_priority(rand):
    priority = []
    A = 55
    M = 1994
    Zo = 10112166
    C = 9
    for i in range(rand):
        LCG = ((A * Zo) + C) % M
        X = LCG / M
        Zo = LCG
        Y = ((3 - 1) * X) + 1
        if Y - np.floor(Y) >= 0.5:
            Y = np.ceil(Y)
            priority.append(int(Y))  # Include the priority as the first element
        else:
            Y = np.floor(Y)
            priority.append(int(Y))

    return priority


# COMPLETION FUNCTION
def custom_priority_completion(arrival, service, priority, num_servers):
    rand = len(arrival)  # Total number of tasks

    # Combine tasks into a list of tuples: (priority, arrival, service, task_index)
    tasks = list(zip(priority, arrival, service, range(rand)))

    # Sort tasks based on priority in ascending order
    tasks.sort()

    # Extract the original indices after sorting
    original_indices = [task[3] for task in tasks]

    # Prioritize the task with arrival time 0
    if arrival[0] == 0:
        original_indices.remove(0)
        original_indices = [0] + original_indices

    # Rearrange tasks based on the custom completion order
    arrival = [arrival[i] for i in original_indices]
    service = [service[i] for i in original_indices]

    # Initialize completion times array
    completion = np.zeros_like(arrival)

    nos = min(num_servers, rand)  # Number of servers

    # Calculate completion times based on service time and number of servers
    for i in range(nos):
        completion[i] = arrival[i] + service[i]

    for i in range(nos, rand):
        max_completion = completion[i - nos]
        for j in range(i - nos + 1, i):
            max_completion = max(max_completion, completion[j] + service[i])
        completion[i] = max_completion + service[i]

    # Rearrange tasks back to their original positions
    completion = [completion[original_indices.index(i)] for i in range(rand)]

    return completion


# M/M/C
def mmc_simulation(arrival_rate, service_rate, nos, spreadsheet, priority):
    # CP (if random is not given / to find random numbers)
    values = []
    i = 0
    # iterate till CP == 1
    while True:
        val = poisson.cdf(k=i, mu=arrival_rate)
        values.append(val)
        if val == 1:
            i += 1
            break
        i += 1
    # length of values is our random number
    rand = len(values)

    # Inter arrivals
    inter_arrival = [0]
    inter_arvl = np.round(np.random.poisson(arrival_rate, size=rand - 1), 2)
    inter_arvl = np.abs(inter_arvl)
    for element in inter_arvl:
        inter_arrival.append(element)

    # Arrivals
    # arrival = np.cumsum(inter_arvl)
    # arrival = np.append(arrival, arrival[-1] + inter_arvl[-1])  # Append the last arrival time
    arrival = [round(sum(inter_arrival[:i + 1]), 2) for i in range(rand)]

    # Services
    service = np.floor(np.random.exponential(scale=1 / service_rate, size=rand) * 10) % 10 + 1
    service = np.abs(service)

    # Priority and Completion
    if priority == 1:
        priority_values = generate_priority(rand)
        completion = np.array(custom_priority_completion(arrival, service, priority_values, nos))

    else:
        priority_values = ['N/A'] * rand

        completion = np.zeros_like(arrival)  # Initialize completion times array
        # Calculate completion times based on service times and number of servers
        for i in range(nos):
            completion[i] = arrival[i] + service[i]

        for i in range(nos, rand):
            completion[i] = max(completion[i - nos], arrival[i]) + service[i]

    # Calculate waiting times and turnaround times
    turnaround_time = completion - arrival
    waiting_time = turnaround_time - service
    response_time = completion - arrival - service

    # Calculate average waiting and turnaround times
    inter_arrival_mean = round(np.mean(inter_arrival), 3)
    arrival_mean = round(np.mean(arrival), 3)
    service_mean = round(np.mean(service), 3)
    avg_turnaround_time = round(np.mean(turnaround_time), 3)
    avg_waiting_time = round(np.mean(np.maximum(waiting_time, 0)), 3)
    avg_response_time = round(np.mean(response_time), 3)

    if spreadsheet == 1:
        default_filename = "Simulation_MMC"
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_filename,
                                                filetypes=[("Excel Files", "*.xlsx")])
        if not filename:
            filename = default_filename  # Use the default filename if the user cancels the dialog

        save_excel(filename, rand, inter_arrival, arrival, service, priority_values,
                   completion, waiting_time, turnaround_time, response_time,
                   inter_arrival_mean, arrival_mean, service_mean,
                   avg_waiting_time, avg_turnaround_time, avg_response_time)
    return arrival_mean, service_mean, avg_turnaround_time, avg_waiting_time, avg_response_time


#avg_arrival, avg_service, Ta, Wt, Res = mmc_simulation(1.58, 2.15, 1, 1, 1)


# M/G/C
def mgc_simulation(arrival_rate, general_distribution, min_mean_shape, max_var_scale, nos, spreadsheet, priority):
    # CP (if random is not given / to find random numbers)
    values = []
    i = 0
    # iterate till CP == 1
    while True:
        val = poisson.cdf(k=i, mu=arrival_rate)
        values.append(val)
        if val == 1:
            i += 1
            break
        i += 1
    # length of values is our random number
    rand = len(values)

    # Inter arrivals
    inter_arrival = [0]
    inter_arvl = np.round(np.random.poisson(arrival_rate, size=rand - 1), 2)
    inter_arvl = np.abs(inter_arvl)
    for element in inter_arvl:
        inter_arrival.append(element)

    # Arrivals
    # arrival = np.cumsum(inter_arvl)
    # arrival = np.append(arrival, arrival[-1] + inter_arvl[-1])  # Append the last arrival time
    arrival = [round(sum(inter_arrival[:i + 1]), 2) for i in range(rand)]

    # Service
    if general_distribution == "Uniform Distribution":
        service = np.round(np.random.uniform(min_mean_shape, max_var_scale, size=rand) * 10) % 10 + 1
        service = np.abs(service)

    elif general_distribution == "Normal Distribution":
        service = np.round(np.random.normal(min_mean_shape, np.sqrt(max_var_scale), size=rand) * 10) % 10 + 1
        service = np.abs(service)

    elif general_distribution == "Gamma Distribution":
        service = np.round(np.random.gamma(min_mean_shape, max_var_scale, size=rand) * 10) % 10 + 1
        service = np.abs(service)

    else:
        raise ValueError("Invalid service distribution")

    # Priority
    if priority == 1:
        priority_values = generate_priority(rand)
        completion = np.array(custom_priority_completion(arrival, service, priority_values, nos))
    else:
        priority_values = ['N/A'] * rand

        # End Time
        completion = np.zeros_like(arrival)  # Initialize completion times array
        # Calculate completion times based on service times and number of servers
        for i in range(nos):
            completion[i] = arrival[i] + service[i]

        for i in range(nos, rand):
            completion[i] = max(completion[i - nos], arrival[i]) + service[i]

    # Calculate waiting times and turnaround times
    turnaround_time = completion - arrival
    waiting_time = turnaround_time - service
    response_time = completion - arrival - service

    # Calculate average waiting and turnaround times
    inter_arrival_mean = round(np.mean(inter_arrival), 3)
    arrival_mean = round(np.mean(arrival), 3)
    service_mean = round(np.mean(service), 3)
    avg_waiting_time = round(np.mean(np.maximum(waiting_time, 0)), 3)
    avg_turnaround_time = round(np.mean(turnaround_time), 3)
    avg_response_time = round(np.mean(response_time), 3)

    if spreadsheet == 1:
        default_filename = "Simulation_MGC"
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_filename,
                                                filetypes=[("Excel Files", "*.xlsx")])
        if not filename:
            filename = default_filename  # Use the default filename if the user cancels the dialog

        save_excel(filename, rand, inter_arrival, arrival, service, priority_values,
                   completion, waiting_time, turnaround_time, response_time,
                   inter_arrival_mean, arrival_mean, service_mean,
                   avg_waiting_time, avg_turnaround_time, avg_response_time)

    return arrival_mean, service_mean, avg_turnaround_time, avg_waiting_time, avg_response_time


# G/G/C
def ggc_simulation(arrival_distribution, service_distribution, min_mean_shape_arvl, min_mean_shape_srvc,
                   max_var_scale_arvl, max_var_scale_srvc, nos, spreadsheet, priority):
    # CP (if random is not given / to find random numbers)
    if arrival_distribution == "Uniform Distribution":
        values = []
        i = 0
        # iterate till CP == 1
        while True:
            val = uniform.cdf(i, loc=min_mean_shape_arvl, scale=max_var_scale_arvl - min_mean_shape_arvl)
            values.append(val)
            if val == 1:
                i += 1
                break
            i += 1
        # length of values is our random number
        rand = len(values)

        # Inter Arrival
        inter_arrival = [0]
        inter_arvl = np.round(np.random.uniform(min_mean_shape_arvl, max_var_scale_arvl, size=rand - 1) * 10) % 10 + 1
        inter_arvl = np.abs(inter_arvl)
        for element in inter_arvl:
            inter_arrival.append(element)

    elif arrival_distribution == "Normal Distribution":
        values = []
        i = 0
        while True:
            val = norm.cdf(i, loc=min_mean_shape_arvl, scale=(np.sqrt(max_var_scale_arvl)))
            values.append(val)
            if val == 1:
                i += 1
                break
            i += 1
        rand = len(values)

        # Inter Arrival
        inter_arrival = [0]
        inter_arvl = np.round(np.random.normal(min_mean_shape_arvl, np.sqrt(max_var_scale_arvl), size=rand - 1) * 10) % 10 + 1
        inter_arvl = np.abs(inter_arvl)
        for element in inter_arvl:
            inter_arrival.append(element)

    elif arrival_distribution == "Gamma Distribution":
        values = []
        i = 0
        while True:
            val = gamma.cdf(i, loc=min_mean_shape_arvl, scale=max_var_scale_arvl)
            values.append(val)
            if val == 1:
                i += 1
                break
            i += 1
        rand = len(values)

        # Inter Arrival
        inter_arrival = [0]
        inter_arvl = np.round(np.random.gamma(min_mean_shape_arvl, max_var_scale_arvl, size=rand - 1) * 10) % 10 + 1
        inter_arvl = np.abs(inter_arvl)
        for element in inter_arvl:
            inter_arrival.append(element)

    else:
        raise ValueError("Invalid service distribution")

    # Arrivals
    # arrival = np.cumsum(inter_arrival)
    # arrival = np.append(arrival, arrival[-1] + inter_arrival[-1])  # Append the last arrival time
    arrival = [round(sum(inter_arrival[:i + 1]), 2) for i in range(rand)]

    # Service
    if service_distribution == "Uniform Distribution":
        service = np.round(np.random.uniform(min_mean_shape_srvc, max_var_scale_srvc, size=rand) * 10) % 10 + 1
        service = np.abs(service)

    elif service_distribution == "Normal Distribution":
        service = np.round(np.random.normal(min_mean_shape_srvc, np.sqrt(max_var_scale_srvc), size=rand) * 10) % 10 + 1
        service = np.abs(service)

    elif service_distribution == "Gamma Distribution":
        service = np.round(np.random.gamma(min_mean_shape_srvc, max_var_scale_srvc, size=rand) * 10) % 10 + 1
        service = np.abs(service)

    else:
        raise ValueError("Invalid service distribution")

    # Priority
    if priority == 1:
        priority_values = generate_priority(rand)
        completion = np.array(custom_priority_completion(arrival, service, priority_values, nos))
    else:
        priority_values = ['N/A'] * rand

        # End Time
        completion = np.zeros_like(arrival)  # Initialize completion times array
        # Calculate completion times based on service times and number of servers
        for i in range(nos):
            completion[i] = arrival[i] + service[i]

        for i in range(nos, rand):
            completion[i] = max(completion[i - nos], arrival[i]) + service[i]

    # Calculate waiting times and turnaround times
    turnaround_time = completion - arrival
    waiting_time = turnaround_time - service
    response_time = completion - arrival - service

    # Calculate average waiting and turnaround times
    inter_arrival_mean = round(np.mean(inter_arrival), 3)
    arrival_mean = round(np.mean(arrival), 3)
    service_mean = round(np.mean(service), 3)
    avg_waiting_time = round(np.mean(np.maximum(waiting_time, 0)), 3)
    avg_turnaround_time = round(np.mean(turnaround_time), 3)
    avg_response_time = round(np.mean(response_time), 3)

    if spreadsheet == 1:
        default_filename = "Simulation_GGC"
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_filename,
                                                filetypes=[("Excel Files", "*.xlsx")])
        if not filename:
            filename = default_filename  # Use the default filename if the user cancels the dialog

        save_excel(filename, rand, inter_arrival, arrival, service, priority_values,
                   completion, waiting_time, turnaround_time, response_time,
                   inter_arrival_mean, arrival_mean, service_mean,
                   avg_waiting_time, avg_turnaround_time, avg_response_time)

    return arrival_mean, service_mean, avg_turnaround_time, avg_waiting_time, avg_response_time


'''
values = ggc_simulation("Normal Distribution", "Normal Distribution", 10, 8, 20, 25, 1)
print(values)
'''
