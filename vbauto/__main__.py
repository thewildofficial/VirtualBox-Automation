import sys,subprocess,re,os
import time
from os import system 
arguments = sys.argv[1:] # takes sys.argv, except thae first element
class colors: # You may need to change color settings
    RED = '\033[31m'
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
vm_list = subprocess.check_output("vboxmanage list vms", shell=True, universal_newlines=True)

def main():
    # checks if arguments is empty
    if len(arguments) == 0:
        print("No parameters provided \n type -h for help menu")

    else:
        if arguments[0] == '-h':
            print("="*30)
            print("-l \t list all machines")
            print("-s \t setup mode")
            print("="*30)
        elif arguments[0] == '-l':
            print(vm_list)
        elif arguments[0] == '-s':
            print(colors.GREEN + "CHOOSE A MACHINE \n" + colors.ENDC)
            i = 1
            name_list = []
            for vm in vm_list.split("\n"):
                try:
                    name = re.findall(r'\".*?\"', vm)[0]
                    name_list.append(name)
                    print(colors.YELLOW + "[" + str(i) + "] " + name + colors.ENDC)
                except:
                    pass
                i+=1
            choice = name_list[int(input(colors.RED+" \n Enter your choice:")) - 1]
            ip = subprocess.check_output("vboxmanage guestproperty get " + choice + " \"/VirtualBox/GuestInfo/Net/0/V4/IP\"",shell=True, universal_newlines=True).split(" ")[1].replace("\n","")
            print (colors.GREEN + "CHOICE:" + choice)
            print(colors.GREEN+"IP:" + ip + colors.ENDC + "\n")
            print(colors.RED)
            username = input("Enter the username: \n")
            print(colors.GREEN + "Turning on machine " + choice + ".Please wait...")
            print(colors.YELLOW)
            system("VBoxManage startvm "+ choice +" --type headless")
            #time.sleep(10)
            print(colors.BLUE + "Starting a new SSH session (" + username + "@" + ip + ").Please Wait... \n")
            os.execlp("ssh", "-oStrictHostKeyChecking=no", "-X",username +"@"+ ip, "-p 22")


if __name__ == '__main__':
    main()

