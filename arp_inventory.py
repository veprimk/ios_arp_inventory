from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from rich.console import Console
from rich.table import Column, Table
import csv


def colorize_row(change_color):
        if change_color is True:
            return 'cyan'
        else:
            return None

def main():

    console = Console()
    
    table = Table(show_header=True, header_style="bold purple")
    table.add_column("Device")
    table.add_column("Protocol", width=12)
    table.add_column("Address")
    table.add_column("Age (min)")
    table.add_column("MAC Address")
    table.add_column("Type")
    table.add_column("Interface")
    
    csv_header = [
        'Device',
        'Protocol',
        'Address',
        'Age',
        'MAC Address',
        'Type',
        'Interface'
    ]
    
    print("Initializing Nornir task....")
    
    nr = InitNornir()
    
    print("Running task...")
    
    result = nr.run(
        task = netmiko_send_command,
        command_string = "show arp"
    )

    print("Getting results...")
    csv_rows = []
    change_color = True
    for device in result:
        for line in result[device][0].result.splitlines():
            res_row = line.split()
            if len(res_row) > 0 and "Protocol" not in res_row[0]:
                table.add_row(device, res_row[0], res_row[1], res_row[2], res_row[3], res_row[4], res_row[5], style=colorize_row(change_color))
                csv_rows.append([device, res_row[0], res_row[1], res_row[2], res_row[3], res_row[4], res_row[5]])
        
        if change_color == True:
            change_color = False
        else:
            change_color = True
        
    console.print(table)

    with open('arp_inventory.csv', 'w') as csvfile:
        my_csv_writer = csv.writer(csvfile)
        my_csv_writer.writerow(csv_header)
        my_csv_writer.writerows(csv_rows)
        
    print("Script job completed!")


if __name__ == "__main__":
    main()
