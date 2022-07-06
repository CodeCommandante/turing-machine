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

#! /usr/bin/python3

import unittest
import machine
import os

class TestTuringMachine(unittest.TestCase):

    def testTuringMachine_1(self):
        Tape = ['a','a']
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertTrue(TM.isInFinalState())
        self.assertEqual(2, TM.getTapeLen())
        Tape.clear()
        del TM

    def testTuringMachine_2(self):
        Tape = ['a','c']
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertFalse(TM.isInFinalState())
        self.assertEqual(2, TM.getTapeLen())
        Tape.clear()
        del TM

    def testTuringMachine_3(self):
        Tape = ['a']
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertTrue(TM.isInFinalState())
        self.assertEqual(1, TM.getTapeLen())
        Tape.clear()
        del TM

    def testTuringMachine_4(self):
        Tape = ['b','b']
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertTrue(TM.isInFinalState())
        self.assertEqual(2, TM.getTapeLen())
        Tape.clear()
        del TM

    def testTuringMachine_5(self):
        Tape = ['b','b','a']
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertTrue(TM.isInFinalState())
        self.assertEqual(3, TM.getTapeLen())
        Tape.clear()
        del TM

    def testTuringMachine_6(self):
        Tape = ['']
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertTrue(TM.isInFinalState())
        self.assertEqual(0, TM.getTapeLen())
        Tape.clear()
        del TM

    def testTuringMachine_7(self):
        Tape = []
        TM = machine.TuringMachine(['q0','q1'],['a','b'],[['q0','a','q0','b','R'],
                                                          ['q0','b','q0','b','R'],
                                                          ['q0','','q1','','L']],'q0',['q1'],Tape)
        Running = True
        while Running:
            Running = TM.move()
        self.assertTrue(TM.isInFinalState())
        self.assertEqual(0, TM.getTapeLen())
        Tape.clear()
        del TM

class TestLanguageAcceptors(unittest.TestCase):

    def testLangAcceptor_empty(self):
        Tape = ''
        try:
            LA = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/empty.txt'))
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def testLangAcceptor_2Lines(self):
        Tape = ''
        try:
            LA = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/two_lines.txt'))
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def testLangAcceptor_goofedTrans(self):
        Tape = 'aabbcc'
        try:
            LA = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/goofedTrans.txt'))
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def testLangAcceptor_a_and_b(self):
        Tape1 = 'ababab'
        Tape2 = 'aaaaa'
        Tape3 = 'bbbbb'
        Tape4 = 'bbaabb'
        Tape5 = 'aacdbb'
        Tape6 = ''
        LA1 = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/a_and_b.txt'))
        LA2 = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/a_and_b.txt'))
        LA3 = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/a_and_b.txt'))
        LA4 = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/a_and_b.txt'))
        LA5 = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/a_and_b.txt'))
        LA6 = machine.LanguageAcceptor(os.path.join(os.path.dirname(__file__), 'TestFiles/a_and_b.txt'))
        self.assertTrue(LA1.run(Tape1,False))
        self.assertTrue(LA2.run(Tape2,False))
        self.assertTrue(LA3.run(Tape3,False))
        self.assertTrue(LA4.run(Tape4,False))
        self.assertFalse(LA5.run(Tape5,False))
        self.assertTrue(LA6.run(Tape6,False))



if __name__ == '__main__':
    unittest.main()