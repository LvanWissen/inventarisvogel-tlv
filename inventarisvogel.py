"""
inventarisvogel

     .-.
    (. .)__,')
    / V      )
    \  (   \/
     `._`._ \

   version 0.1
"""

import os
import shutil

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.focusmodel('passive')
root.withdraw()


class Vogel:
    """
    Command line application for stock taking and file preparation in titelive medialog inventory software.
    """

    def __init__(self, folder="stock", format="TiteLive", logdir='log'):
        print(__doc__)

        self.img = """
     .-.
    (. .)__,')
    / V      )
    \  (   \/
     `._`._ \

              """

        self.folder = folder
        self.logdir = logdir
        self.checkdir(self.folder)
        self.checkdir(self.logdir)

        self.format = format

        self.history = dict()


    def start(self):
        """
        Start user input sequence
        """

        #  start sequence
        stop = False
        while stop is False:
            print(self.img)
            print("Choose an option from the list: ")
            print("""
          1. Add zone
          2. Exit
                  """)
            userinput = input("")


            if userinput == '1':
                stop_zone = False
                while stop_zone is False:
                    zone = input("Zone number: ")

                    if int(zone) in self.history:
                        print()
                        print("Warning! Zone already used! Overwriting file! ")
                        print("Do you want to continue?")
                        print("""
          1. Continue [ENTER]
          2. Return
                            """)
                        if input() == '2':
                            stop_zone = True
                            continue

                    print("Add zone '{}'".format(zone))
                    print("----------")
                    print("Choose an option from the list: ")
                    print("""
          1. File input
          2. Scanner input
          3. Return
                      """)

                    userinput = input("")

                    if userinput == '1':
                        self.addzone(zone, itype='file')
                        stop_zone = True
                    elif userinput == '2':
                        self.addzone(zone, itype='scanner')
                        stop_zone = True
                    elif userinput == '3':
                        stop_zone = True
                    else:
                        print("Not a valid input. Pick a number. ")

            elif userinput == '2':
                stop = True




    def addzone(self, zone=-1, itype='file'):
        """
        Add zone through:
            1. file
            2. direct scanner input

        Stores a copy in the log directory and writes the prepared
        file in the stock directory. 

        """
        if zone == -1:
            zone = str(int(input("Zone number: "))).zfill(4)

        else:
            zone = str(int(zone)).zfill(4)

        print("Zone: {}".format(zone))

        #  FILE
        if itype == 'file':
            filepath = filedialog.askopenfilename()
            self.checkfile(filepath)

            filepath = shutil.copy(filepath, self.logdir + os.sep + zone + '.txt')  # don't mess with the original

            isbns = self.parsefile(filepath)

            self.writefile(isbns, zone)

        # #  FOLDER
        # folderpath = filedialog.askdirectory()
        # self.checkdir(folderpath, create=False)

        # files = os.listdir(folderpath)

        # filepaths = []
        # for file in files:
        #     filepaths.append(shutil.copy(file, self.logdir + os.sep + zone + '.txt'))

        #  SCANNER
        if itype == 'scanner':
            isbns = []

            print("Input isbns through scanner. End this input method by typing 'exit'.")

            exit = False
            while exit is False:
                i = input()

                if i == 'exit':
                    exit = True
                elif i.isnumeric():
                    isbns.append(i)

            # logging isbn sequence
            with open(self.logdir + os.sep + zone + '.txt', 'w', encoding='utf-8') as logfile:
                for i in isbns:
                    logfile.write(i)
                    logfile.write('\n')

            # writing file
            self.writefile(isbns, zone)



    def checkdir(self, folder, create=True):
        """
        Checks if dir exists, otherwise create it.
        """
        if not os.path.isdir(folder) and create:
            try:
                os.makedirs(folder)
                print("Created dir '{}' at location '{}'.".format(os.path.basename(folder), os.path.abspath(folder)))
            except:
                raise OSError("Cannot create dir")
        elif os.listdir() and create:
            print("Folder '{}' not empty".format(folder))

    def checkfile(self, filepath):
        """
        Checks if file contains numeric values. Otherwise, raise an error. 
        """

        with open(filepath) as infile:
            lines = infile.readlines()
            n_lines = sum(1 for x in lines if x != '')

            if n_lines and ''.join([l.strip() for l in lines]).isnumeric():
                return n_lines
            else:
                raise EnvironmentError("File malformed")

    def parsefile(self, filepath):
        """
        Parse a file and return a list of strings (EAN).
        """

        with open(filepath, encoding='utf-8') as infile:
            isbns = [i for i in infile.read().split('\n') if i]

        return isbns

    def writefile(self, isbns, zone):
        """
        Writes file to stock dir in format:
            0001,9789012345678,0001.
        """
        filepath = self.folder + os.path.sep + zone + '.txt'
        with open(filepath, 'w', encoding='utf-8') as outfile:

            for i in isbns:
                s = "{zone},{isbn},{quant}".format(zone=zone, isbn=i, quant='0001')

                outfile.write(s)
                outfile.write('\n')

        self.history[int(zone)] = isbns  # add to history
        print("Written {} isbns to file '{}'".format(len(isbns), filepath))


if __name__ == "__main__":
    v = Vogel()
    v.start()
