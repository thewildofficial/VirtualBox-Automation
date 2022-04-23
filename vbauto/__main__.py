import sys,subprocess,re,os,time
from os import system
from rich.console import Console
from rich import print as pprint

import typer
from ssh_wait import ssh_wait

#Global Variables
console = Console()
app = typer.Typer()

def find_name(name): # returns the name surrounded by ", instead of a UID
        return re.findall(r'\".*?\"', name)[0]
def get_choice(list):
    pprint("[green] Choose A Machine [/green] \n")
    for vm in enumerate(list):
            if vm[1] != "":
                name = find_name(vm[1]) #searches the string for " and returns the string between the quotes
                pprint(f"[yellow] {vm[0] + 1} [/yellow] {name}")
    try:
        return find_name(list[int(console.input("[red] Enter your choice: [/red] ")) - 1])
    except:
        pprint("[red] Invalid Choice [/red]")
        exit(-1)
@app.command()
def restart():
    name = get_choice(subprocess.check_output("vboxmanage list runningvms", shell=True, universal_newlines=True).split("\n"))
    try:
        system(f"vboxmanage controlvm {name} poweroff soft")
        system(f"VBoxManage startvm {name} --type headless")
        pprint(f"[green] Machine {name} has been restarted [/green]")
    except Exception as e:
        pprint(f"[red] Restart Failed [/red]")
@app.command()
def shutdown():
    name = get_choice(subprocess.check_output("vboxmanage list runningvms", shell=True, universal_newlines=True).split("\n"))
    try:
        shutdown_message = subprocess.check_output(f"vboxmanage controlvm {name} poweroff soft",shell=True, universal_newlines=True)
        pprint(f"[green] Machine {name} is now powered off [/green]")
    except:
        pprint(f"[red] Machine {name} is already powered off [/red]")
@app.command()
def setup(ssh: bool = True,headless:bool =True):
    choice = get_choice(subprocess.check_output("vboxmanage list vms", shell=True, universal_newlines=True).split("\n"))
    state = subprocess.check_output(f"VBoxManage showvminfo {choice} | grep State",shell=True, universal_newlines=True).split("                       ")
    ip = subprocess.check_output(f"vboxmanage guestproperty get {choice} \"/VirtualBox/GuestInfo/Net/0/V4/IP\"",shell=True, universal_newlines=True).split(" ")[1].replace("\n","") #gets the ip address of the vm
    pprint (f"[green]CHOICE: {choice} [/green]")
    pprint(f"[green] IP: {ip} [/green]")
    pprint(f"[green]State: {state[1]} [/green]")
    pprint(f"[green]Turning on your machine...[/green]")
    try:
         headless_option = "--type headless" if headless else " "
         system(f"VBoxManage startvm {choice} {headless_option}")
         pprint("[green] SUCCESS! [/green] Machine is on!")
    except:
         pprint("[red] FAILURE! [/red] Something went wrong while turning on your machine, aborting...")
         exit(-1)
    if ssh:
        username = console.input("[red] Enter your username: [/red] ")
        pprint("[blue]Waiting for SSH to be available...[/blue]")
        time.sleep(5)
        ssh_result = ssh_wait(ip,service=22)
        if ssh_result == 0:
            # SSH into the container
            pprint("[blue]=> SSH available! Logging in...[/blue]")
            os.execlp("ssh", "-oStrictHostKeyChecking=no", "-X", f"{username}@{ip}")
        else:
            pprint(
                "[red]: FAILURE! [/red] Timeout waiting for SSH to available in the VM, check if SSH service is available in the VM and the IP is reachable")
            exit(-1)
    else:
       pprint(f"SSH is [red]disabled[/red], but you can interact with the machine at {ip}")


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        pprint("[bold red]=> CTRL+C Received. Exiting...[/bold red]")
        exit(0)
