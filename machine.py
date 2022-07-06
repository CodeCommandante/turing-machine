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

import time

InputExceptionMessage = 'Machine definition file incorrect or incomplete.'
DEBUG = False

class TuringMachine:
    __States = []
    __Alpha = []
    __TransFuncs = []
    __CurrState = ''
    __FinalStates = []
    __Tape = []
    __TapeIndex = 0

    def __init__(self, States: list, Alpha: list, TransFuncs: list, InitState: str, FinalStates: list, Tape: list):
        self.__States = States.copy()
        self.__Alpha = Alpha.copy()
        self.__TransFuncs = TransFuncs.copy()
        self.__CurrState = InitState
        self.__FinalStates = FinalStates.copy()
        self.__Tape = Tape.copy()

    def __del__(self):
        self.__States.clear()
        self.__Alpha.clear()
        self.__TransFuncs.clear()
        self.__FinalStates.clear()
        self.__Tape.clear()

    def __getTransOn(self, CurrSym: str) -> list:
        for i in self.__TransFuncs:
            if i[0] == self.__CurrState and i[1] == CurrSym:
                return i.copy()
        return []

    def __trimTape(self):
        TempTape = []
        for i in self.__Tape:
            if not i == '':
                TempTape.append(i)
        self.__Tape.clear()
        self.__Tape = TempTape.copy()
        TempTape.clear()

    def getCurrentIndex(self) -> int:
        return self.__TapeIndex

    def getCurrentState(self) -> str:
        return self.__CurrState

    def getCurrentTape(self) -> list:
        #self.__trimTape()
        return self.__Tape.copy()

    def getTapeLen(self) -> int:
        self.__trimTape()
        return len(self.__Tape)

    def isInFinalState(self) -> bool:
        for i in self.__FinalStates:
            if i == self.__CurrState:
                return True
        return False

    def move(self) -> bool:
        Trans = []
        #Check array boundary conditions
        if (self.__TapeIndex < 0) or (self.__TapeIndex >= len(self.__Tape)):
            Trans = self.__getTransOn('')
        else:
            Trans = self.__getTransOn(self.__Tape[self.__TapeIndex])
        #If returned empty array, halt state
        if len(Trans) == 0:
            return False
        #Else, perform insert/append/replace
        elif self.__TapeIndex < 0:
            self.__Tape.insert(0,Trans[3])
        elif self.__TapeIndex >= len(self.__Tape):
            self.__Tape.append(Trans[3])
        else:
            self.__Tape[self.__TapeIndex] = Trans[3]
        #Move left or right or throw exception
        if Trans[4] == 'L':
            self.__TapeIndex = self.__TapeIndex - 1
        elif Trans[4] == 'R':
            #Special case:  if 'deleting' 0 index, don't advance index.
            if Trans[3] == '' and self.__TapeIndex == 0:
                pass
            else:
                self.__TapeIndex = self.__TapeIndex + 1
        else:
            raise Exception('Machine move definition incorrect or undefined.')
        #Update current state
        self.__CurrState = Trans[2]
        self.__trimTape()
        return True

class LanguageAcceptor:

    __TM = ()
    __States = []
    __Alpha = []
    __TransFuncs = []
    __InitState = ''
    __FinalStates = []
    __Tape = ''

    def __init__(self, FileName: str):
        Fin = open(FileName, 'r')
        FileRead = Fin.readlines()
        FileLen = len(FileRead)
        if FileLen < 3:
            Fin.close()
            raise Exception(InputExceptionMessage)
        #Build transition funcs, states, alpha
        try:
            for t in range(FileLen - 2):
                self.__TransFuncs.append(self.__buildTransition(FileRead[t]))
            self.__buildStates()
            self.__buildAlpha()
            self.__InitState = FileRead[FileLen - 2].strip()
            self.__buildFinals(FileRead[FileLen - 1])
            Fin.close()
        except:
            Fin.close()

    def __del__(self):
        self.__States.clear()
        self.__Alpha.clear()
        self.__TransFuncs.clear()
        self.__FinalStates.clear()

    def __buildAlpha(self):
        for i in self.__TransFuncs:
            if len(i[1]) > 1 or len(i[3]) > 1:
                raise Exception(InputExceptionMessage)
            elif len(i[0]) == 1 and not self.__isDuplicate(i[1],self.__Alpha):
                self.__Alpha.append(i[1])
            elif len(i[3]) == 1 and not self.__isDuplicate(i[3],self.__Alpha):
                self.__Alpha.append(i[3])

    def __buildFinals(self, Line: str):
        Parts = Line.split(',')
        for fs in Parts:
            self.__FinalStates.append(fs.strip())

    def __buildStates(self):
        for i in self.__TransFuncs:
            if not self.__isDuplicate(i[0],self.__States):
                self.__States.append(i[0])
            if not self.__isDuplicate(i[2],self.__States):
                self.__States.append(i[2])

    def __buildTransition(self, Line: str) -> list:
        Parts = Line.split('->')
        if not len(Parts) == 2:
            raise Exception(InputExceptionMessage)
        Leftside = Parts[0].strip()
        Rightside = Parts[1].strip()
        LeftSplit = Leftside.split(',')
        RightSplit = Rightside.split(',')
        if len(LeftSplit) > 2 or len(LeftSplit) < 1 or not len(RightSplit) == 3:
            raise Exception(InputExceptionMessage)
        TotalBuild = []
        if len(LeftSplit) == 1:
            TotalBuild.append(LeftSplit[0].strip())
            TotalBuild.append('')
        else:
            TotalBuild.append(LeftSplit[0].strip())
            TotalBuild.append(LeftSplit[1].strip())
        TotalBuild.append(RightSplit[0].strip())
        TotalBuild.append(RightSplit[1].strip())
        TotalBuild.append(RightSplit[2].strip())
        return TotalBuild.copy()

    def __isDuplicate(self, Sym: str, List: list) -> bool:
        if len(List) > 0:
            for i in List:
                if i == Sym:
                    return True
        return False

    def printAlpha(self):
        print(self.__Alpha)

    def printFinalStates(self):
        print(self.__FinalStates)

    def printInitialState(self):
        print(self.__InitState)

    def printStates(self):
        print(self.__States)
    
    def printTransitions(self):
        for p in self.__TransFuncs:
            print(p)

    def run(self, Tape: str, View = True) -> bool:
        self.__TM = TuringMachine(self.__States, self.__Alpha, self.__TransFuncs, self.__InitState, self.__FinalStates, list(Tape))
        Running = True
        if View:
            print(Tape)
        while Running:
            Plist = self.__TM.getCurrentTape()
            Pstr = ''.join(Plist)
            if View and not DEBUG:
                print('                                  \r' + Pstr,'\r', end='')
                time.sleep(0.10)
            Running = self.__TM.move()
            if DEBUG:
                print(self.__TM.getCurrentState(),' ',Pstr)
        if View and not DEBUG:
            print('\n')
        return self.__TM.isInFinalState()

class Transducer:

    __TM = ()
    __States = []
    __Alpha = []
    __TransFuncs = []
    __InitState = ''
    __FinalStates = []
    __Tape = ''

    def __init__(self, FileName: str):
        Fin = open(FileName, 'r')
        FileRead = Fin.readlines()
        FileLen = len(FileRead)
        if FileLen < 3:
            Fin.close()
            raise Exception(InputExceptionMessage)
        #Build transition funcs, states, alpha
        try:
            for t in range(FileLen - 2):
                self.__TransFuncs.append(self.__buildTransition(FileRead[t]))
            self.__buildStates()
            self.__buildAlpha()
            self.__InitState = FileRead[FileLen - 2].strip()
            self.__buildFinals(FileRead[FileLen - 1])
            Fin.close()
        except:
            Fin.close()

    def __del__(self):
        self.__States.clear()
        self.__Alpha.clear()
        self.__TransFuncs.clear()
        self.__FinalStates.clear()

    def __buildAlpha(self):
        for i in self.__TransFuncs:
            if len(i[1]) > 1 or len(i[3]) > 1:
                raise Exception(InputExceptionMessage)
            elif len(i[0]) == 1 and not self.__isDuplicate(i[1],self.__Alpha):
                self.__Alpha.append(i[1])
            elif len(i[3]) == 1 and not self.__isDuplicate(i[3],self.__Alpha):
                self.__Alpha.append(i[3])

    def __buildFinals(self, Line: str):
        Parts = Line.split(',')
        for fs in Parts:
            self.__FinalStates.append(fs.strip())

    def __buildStates(self):
        for i in self.__TransFuncs:
            if not self.__isDuplicate(i[0],self.__States):
                self.__States.append(i[0])
            if not self.__isDuplicate(i[2],self.__States):
                self.__States.append(i[2])

    def __buildTransition(self, Line: str) -> list:
        Parts = Line.split('->')
        if not len(Parts) == 2:
            raise Exception(InputExceptionMessage)
        Leftside = Parts[0].strip()
        Rightside = Parts[1].strip()
        LeftSplit = Leftside.split(',')
        RightSplit = Rightside.split(',')
        if len(LeftSplit) > 2 or len(LeftSplit) < 1 or not len(RightSplit) == 3:
            raise Exception(InputExceptionMessage)
        TotalBuild = []
        if len(LeftSplit) == 1:
            TotalBuild.append(LeftSplit[0].strip())
            TotalBuild.append('')
        else:
            TotalBuild.append(LeftSplit[0].strip())
            TotalBuild.append(LeftSplit[1].strip())
        TotalBuild.append(RightSplit[0].strip())
        TotalBuild.append(RightSplit[1].strip())
        TotalBuild.append(RightSplit[2].strip())
        return TotalBuild.copy()

    def __isDuplicate(self, Sym: str, List: list) -> bool:
        if len(List) > 0:
            for i in List:
                if i == Sym:
                    return True
        return False

    def printAlpha(self):
        print(self.__Alpha)

    def printFinalStates(self):
        print(self.__FinalStates)

    def printInitialState(self):
        print(self.__InitState)

    def printStates(self):
        print(self.__States)
    
    def printTransitions(self):
        for p in self.__TransFuncs:
            print(p)

    def run(self, Tape: str, View = True) -> bool:
        self.__TM = TuringMachine(self.__States, self.__Alpha, self.__TransFuncs, self.__InitState, self.__FinalStates, list(Tape))
        Running = True
        if View:
            print(Tape)
        while Running:
            Plist = self.__TM.getCurrentTape()
            Pstr = ''.join(Plist)
            if View and not DEBUG:
                print('                                  \r' + Pstr,'\r', end='')
                time.sleep(0.10)
            Running = self.__TM.move()
            if DEBUG:
                print(self.__TM.getCurrentState(),' ',Pstr)
        if View and not DEBUG:
            print('\n')
        return self.__TM.isInFinalState()
