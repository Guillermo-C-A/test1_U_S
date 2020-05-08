from consolemenu import *
from consolemenu.items import *
import os
import inquirer
from subprocess import call

class ZFS():

    def __init__(self):

        all_disks = os.popen("lsblk  -d -e7").read().split("\n")
        self.all_disks = all_disks[1:len(all_disks)-1]
        self.types = [
                        "mirror"
                    ]
        self.selected_disks = []
        self.zfs_option = ''
    
    def print_disks(self):

        f = os.popen("lsblk -e7").read()
        print(f)
        input("PRESS ENTER")
    
    def zfs_status(self):

        info = os.popen("zpool status").read()
        print(info)
        input("PRESS ENTER")

    def option_menu(self, title, options):

        questions = [inquirer.Checkbox(
            'interests',
            message=title,
            choices=options,
        )]
        answers = inquirer.prompt(questions)
        
        return answers['interests']

    def list_option(self, title, options):

        questions = [inquirer.List(
            'interests',
            message=title,
            choices=options,
        )]
        answers = inquirer.prompt(questions)
        
        return answers['interests']       

    def get_disks(self):
        
        self.selected_disks = self.option_menu("Select disk for the zfs pool", self.all_disks)

    def get_type(self):

        print("Selected_disks: \n")
        for disk in self.selected_disks:
            print(disk)
        print()
        
        self.zfs_option = self.list_option("ZFS poll type", self.types)
    
    def create_zfs(self):

        print(f"ZFS type: {self.zfs_option} \n")

        print("Selected_disks: \n")
        for disk in self.selected_disks:
            print(disk)

        print("\n")
        user = self.list_option("Create ZFS", ["YES", "NO"])
        
        if user == "YES":
            
            foo = lambda x: "/dev/" + x.split(' ')[0]
            disks = list(map(foo,  self.selected_disks))
            name = input("Poll name: ")

            f = ["zpool", "create", name, self.types[0]] + disks

            print(f)
            input()



menu = ConsoleMenu("ZFS MENU")

my_zfs = ZFS()

disk_list = FunctionItem("List all disks", my_zfs.print_disks)
select_disk = FunctionItem("Select disk", my_zfs.get_disks)
select_type = FunctionItem("Select ZFS type", my_zfs.get_type)
create_zfs = FunctionItem("Create ZFS", my_zfs.create_zfs)
zfs_status = FunctionItem("ZFS status", my_zfs.zfs_status)

menu.append_item(disk_list)
menu.append_item(select_disk)
menu.append_item(select_type)
menu.append_item(create_zfs)
menu.append_item(zfs_status)

menu.show()