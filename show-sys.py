from turtle import clear
import Pmw
import psutil
import platform
import threading
import tkinter as tk
import pandas as pd
from datetime import datetime

def get_size(bytes, suffix='B'):
    factor = 1024
    for unit in ['','K','M','G','T','P']:
        if bytes < factor:
            return f'{bytes:.2f}{unit}{suffix}'
        bytes /= factor

print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")

print("="*40, "CPU Info", "="*40)
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))

cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
    print(f"Core {i}: {percentage}%")

print("="*40, "Memory Information", "="*40)
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")

print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f" Mountpoint: {partition.mountpoint}")
    print(f" File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    print(f" Total Size: {get_size(partition_usage.total)}")
    print(f" Used: {get_size(partition_usage.used)}")
    print(f" Free: {get_size(partition_usage.free)}")
    print(f" Percentage: {partition_usage.percent}%")
# disk_io = psutil.disk_io_counters()
# print(f"Total read: {get_size(disk_io.read_bytes)}")
# print(f"Total write: {get_size(disk_io.write_bytes)}")

print("="*40, "Network Information", "="*40)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

ventana = tk.Tk()
#color de la ventana gris oscuro
ventana.configure(bg='#2d2d2d')
display = Pmw.ScrolledText(hscrollmode ='none',
                           vscrollmode = 'dynamic', hull_relief='sunken',
                           hull_background='gray20', hull_borderwidth=10,
                           text_background='black', text_width=109,
                           text_foreground='white', text_height=39,
                           text_padx=10, text_pady=10, text_relief='groove',
                           text_font=('Fixedsys',10))
display.pack(padx = 0, pady = 0)

botones = Pmw.ButtonBox(ventana)
botones.pack(fill='both', expand=1, padx=1, pady=1)
# disk_io = psutil.disk_io_counters()
    # display.appendtext(f"Total read: {get_size(disk_io.read_bytes)}\n")
    # display.appendtext(f"Total write: {get_size(disk_io.write_bytes)}\n")

def inicia(index):
    infos = {0:system, 1:cpu, 2:memory, 3:disk, 4:network}
    t= threading.Thread(target=infos[index])
    t.start()

def memory():
    display.appendtext(("="*40)+"Memory Information"+(("=")*40)+"\n")
    svmem = psutil.virtual_memory()
    display.appendtext(f"Total: {get_size(svmem.total)}\n")
    display.appendtext(f"Available: {get_size(svmem.available)}\n")
    display.appendtext(f"Used: {get_size(svmem.used)}\n")
    display.appendtext(f"Percentage: {svmem.percent}%\n")
    display.appendtext(("="*20)+ "SWAP"+("="*20)+"\n")
    swap = psutil.swap_memory()
    display.appendtext(f"Total: {get_size(swap.total)}\n")
    display.appendtext(f"Free: {get_size(swap.free)}\n")
    display.appendtext(f"Used: {get_size(swap.used)}\n")
    display.appendtext(f"Percentage: {swap.percent}%\n")
    
def system():
    display.appendtext(("="*40)+"System Information"+(("=")*40)+"\n")
    uname = platform.uname()
    display.appendtext(f"System: {uname.system}\n")
    display.appendtext(f"Node Name: {uname.node}\n")
    display.appendtext(f"Release: {uname.release}\n")
    display.appendtext(f"Version: {uname.version}\n")
    display.appendtext(f"Machine: {uname.machine}\n")
    display.appendtext(f"Processor: {uname.processor}\n")

def cpu():
    display.appendtext(("="*41)+"CPU Information"+(("=")*41)+"\n")
    display.appendtext(("Physical cores: "+str(psutil.cpu_count(logical=False))))
    display.appendtext("\n")
    display.appendtext(("Total cores: "+str(psutil.cpu_count(logical=True))))
    display.appendtext("\n")
    cpufreq = psutil.cpu_freq()
    display.appendtext(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    display.appendtext(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    display.appendtext(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
    display.appendtext("CPU Usage Per Core: \n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        display.appendtext(f"Core {i}: {percentage}%\n")
        display.appendtext(f"Total CPU Usage: {psutil.cpu_percent()}%\n")

def disk():
    display.appendtext(("="*40)+"Disk Information"+(("=")*40)+"\n")
    display.appendtext("Partitions and Usage:")
    display.appendtext("\n")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        display.appendtext(f"=== Device: {partition.device} ===\n")
        display.appendtext(f" Mountpoint: {partition.mountpoint}\n")
        display.appendtext(f" File system type: {partition.fstype}\n")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        display.appendtext(f" Total Size: {get_size(partition_usage.total)}\n")
        display.appendtext(f" Used: {get_size(partition_usage.used)}\n")
        display.appendtext(f" Free: {get_size(partition_usage.free)}\n")
        display.appendtext(f" Percentage: {partition_usage.percent}%\n")

def network():
    display.appendtext(("="*40)+"Network Information"+(("=")*40)+"\n")
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            display.appendtext(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                display.appendtext(f"  IP Address: {address.address}\n")
                display.appendtext(f"  Netmask: {address.netmask}\n")
                display.appendtext(f"  Broadcast IP: {address.broadcast}\n")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                display.appendtext(f"  MAC Address: {address.address}\n")
                display.appendtext(f"  Netmask: {address.netmask}\n")
                display.appendtext(f"  Broadcast MAC: {address.broadcast}\n")
    net_io = psutil.net_io_counters()
    display.appendtext(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n")
    display.appendtext(f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n")

def clear():
    display.clear()
    display.appendtext('USE THE BUTTONS TO SELECT THE INFORMATION. \n\n')    

botones.add('System info', command = lambda:inicia(0), width = 15, bg= 'grey')
botones.add('CPU info', command = lambda:inicia(1), width = 15, bg= 'grey')
botones.add('Memory info', command = lambda:inicia(2), width = 15, bg= 'grey')
botones.add('Disk info', command = lambda:inicia(3), width = 15, bg= 'grey')
botones.add('Network info', command = lambda:inicia(4), width = 15, bg= 'grey')
botones.add('CLEAR', command=clear, bg = 'grey')
botones.alignbuttons()
clear()

ventana.title('Auditoria R-System')
ventana.mainloop()

def get_size(bytes, suffix = 'B'):
    factor = 1024
    for unit in ['','K','M','G','T','P']:
        if bytes < factor:
            return f'{bytes:.2f}{unit}{suffix}'
        bytes /= factor
