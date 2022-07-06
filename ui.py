"""    
    Program simulating a single-tape Turing Machine.
    Copyright (C) 2021  Jim Leon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import machine
import os

VIEW_PROCESS = True

class UI:

    __CurrSelect = 0

    def __init__(self):
        self.displayProgramDesc()
        Status = True
        while Status:
            if self.__CurrSelect == 0:
                self.__CurrSelect = self.mainMenu()
            elif self.__CurrSelect == 1:
                self.__CurrSelect = self.langAcceptorMenu()
            elif self.__CurrSelect == 2:
                self.__CurrSelect = self.adderMenu()
            elif self.__CurrSelect == 3:
                self.__CurrSelect = self.multiMenu()
            elif self.__CurrSelect == 4:
                self.__CurrSelect = self.custTransducer()
            else:
                Status = False
                print('Goodbye!')

    def __del__(self):
        pass

    def __describeUserFile(self):
        print('\n')
        print('Machine description file must be of the following format:')
        print('---------------------------------------------------------')
        print(' => First n lines must describe the transition functions ')
        print('    of the form:  state, symbol -> state, symbol, moveDir')
        print('    where \'state\' and \'symbol\' are variables and ')
        print('    \'moveDir\' is either \'L\' or \'R\', for move Left or')
        print('    move Right, respectively.')
        print(' => \'symbol\' must be a single character.')
        print(' => You must include the commas and \'->\' delimiter in the') 
        print('    description.')
        print(' => For transitions on "blank", insert empty space between the') 
        print('    commas and/or delimiters.  (See included .txt files for examples.')
        print(' => No empty lines in the file.')
        print(' => After transitions, a line describing the starting state.')
        print(' => After starting state, a comma separated list of the ')
        print('    final states on the machine.  This is a single line.')
        print('\n')

    def adderMenu(self) -> int:
        print('')
        print('-------------------------- Adders ----------------------------')
        print('1.  Add unary numbers (e.g. 111+1111)')
        print('2.  Add binary numbers (e.g. 010110+000011)')
        print('3.  Back to Main Menu')
        print('')
        UserIn = input('Selection:  ')
        try:
            int(UserIn)
        except:
            print('Invalid selection.')
            return 2
        if (int(UserIn) < 1) or (int(UserIn) > 3):
            print('Invalid selection.')
            return 2
        elif int(UserIn) == 1:
            AddM = machine.Transducer(os.path.join(os.path.dirname(__file__), 'machDescriptions/addUnary.txt'))
            Tape = input('Enter the two numbers to add, seperated by a \'+\' symbol (i.e. 111+1111):  ')
            InLang = AddM.run(Tape,VIEW_PROCESS)
            if not InLang:
                print('Input format invalid.  Try again!')
            del AddM
            return 2
        elif int(UserIn) == 2:
            AddM = machine.Transducer(os.path.join(os.path.dirname(__file__), 'machDescriptions/addBinary.txt'))
            Tape = input('Enter the two numbers to add, seperated by a \'+\' symbol (i.e. 0111+0101).  Both numbers must be the same length and should have a 0 for their most significant bit:  ')
            InLang = AddM.run(Tape,VIEW_PROCESS)
            if not InLang:
                print('Input format invalid.  Try again!')
            del AddM
            return 2
        else:
            return 0  

    def custTransducer(self):
        self.__describeUserFile()
        FileLoc = input('Enter the name of the file, including it\'s relative path from \nthis working directory:  ')
        try:
            Tsdcr = machine.Transducer(os.path.join(os.path.dirname(__file__),FileLoc))
            Tape = input('\nEnter calculation to run here:  ')
            InLang = Tsdcr.run(Tape,VIEW_PROCESS)
            if not InLang:
                print('Calculation incomplete!  Check your machine description file?')
            del Tsdcr
        except:
            print('\nCould not locate file!  Please check path and/or file name and try again.')
        return 0

    def displayProgramDesc(self):
        print('')
        print('THE TURING MACHINE SIMULATOR')
        print('==============================================================')
        print('This program simulates various uses for the Turing Machine.  ')
        print('Author:  Jim Leon')
        print('')

    def langAcceptorMenu(self) -> int:
        print('')
        print('-------------------- Language Acceptors ----------------------')
        print('1.  L = {(a^n)(b^n)(c^n), n > 0}')
        print('2.  L = {w w^R, |w w^R| is even, \u03A3 = (a,b)}')
        print('3.  Import custom language acceptor from file')
        print('4.  Back to Main Menu')
        print('')
        UserIn = input('Selection:  ')
        try:
            int(UserIn)
        except:
            print('Invalid selection.')
            return 1
        if (int(UserIn) < 1) or (int(UserIn) > 4):
            print('Invalid selection.')
            return 1
        elif int(UserIn) == 1:
            LA = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'machDescriptions/anbncn.txt'))
            Tape = input('Enter the comparing string:  ')
            InLang = LA.run(Tape,VIEW_PROCESS)
            if InLang:
                print(Tape, 'is in the language!')
            else:
                print(Tape, 'is not in the language!')
            del LA
            return 1
        elif int(UserIn) == 2:
            LA = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__),'machDescriptions/wwR.txt'))
            Tape = input('Enter the comparing string:  ')
            InLang = LA.run(Tape,VIEW_PROCESS)
            if InLang:
                print(Tape, 'is in the language!')
            else:
                print(Tape, 'is not in the language!')
            del LA
            return 1
        elif int(UserIn) == 3:
            self.__describeUserFile()
            FileLoc = input('Enter the name of the file, including it\'s relative path from \nthis working directory:  ')
            try:
                LA = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__),FileLoc))
                Tape = input('\nEnter the comparing string:  ')
                InLang = LA.run(Tape,VIEW_PROCESS)
                if InLang:
                    print(Tape, 'is in the language!')
                else:
                    print(Tape, 'is not in the language!')
                del LA
            except:
                print('\nCould not locate file!  Please check path and/or file name and try again.')
            return 1
        else:
            return 0     

    def mainMenu(self) -> int:
        print('')
        print('------------------------- Main Menu --------------------------')
        print('1.  Language Acceptors')
        print('2.  Adders')
        print('3.  Multiply & Divide')
        print('4.  Import custom transducer from file')
        print('5.  Exit Application')
        print('')
        UserIn = input('Selection:  ')
        try:
            int(UserIn)
        except:
            print('Invalid selection.')
            return 0
        if (int(UserIn) < 1) or (int(UserIn) > 5):
            print('Invalid selection.')
            return 0
        return int(UserIn)

    def multiMenu(self) -> int:
        print('')
        print('----------------------- Multiply & Divide --------------------------')
        print('1.  Multiply unary numbers (e.g. 111*11 = 111111)')
        print('2.  Divide unary numbers (e.g. 111111/11 = 111)')
        print('3.  Back to Main Menu')
        print('')
        UserIn = input('Selection:  ')
        try:
            int(UserIn)
        except:
            print('Invalid selection.')
            return 3
        if (int(UserIn) < 1) or (int(UserIn) > 3):
            print('Invalid selection.')
            return 3
        elif int(UserIn) == 1:
            Multi = machine.Transducer(os.path.join(os.path.dirname(__file__), 'machDescriptions/unaryMultiply.txt'))
            Tape = input('Enter the two numbers to multiply, seperated by a \'*\' symbol (i.e. 111*1111):  ')
            InLang = Multi.run(Tape,VIEW_PROCESS)
            if not InLang:
                print('Input format invalid.  Try again!')
            del Multi
            return 3
        elif int(UserIn) == 2:
            Divid = machine.Transducer(os.path.join(os.path.dirname(__file__), 'machDescriptions/unaryDivide.txt'))
            Tape = input('Enter the two numbers to add, seperated by a \'/\' symbol (i.e. 1111/11):  ')
            InLang = Divid.run(Tape,VIEW_PROCESS)
            if not InLang:
                print('Input format invalid.  Try again!')
            del Divid
            return 3
        else:
            return 0 