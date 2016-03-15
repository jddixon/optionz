#!/usr/bin/python3

# testOptionz.py

import os, time, unittest

from rnglib         import SimpleRNG
from optionz    import Optionz as Z
from optionz    import (ZOption, BoolOption, ChoiceOption,
                            FloatOption, IntOption, ListOption, StrOption)

class TestOptionz (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG( time.time() )
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
    
    def testBareOptionz (self):
        myOptz = Z('fred')
        self.assertEqual(myOptz.name,         'fred')
        self.assertEqual(myOptz.desc,          None)
        self.assertEqual(myOptz.epilog,        None)
        self.assertEqual(len(myOptz),          0)

        myOptz = Z('frank', 'frivolous', 'fabulous')
        self.assertEqual(myOptz.name,         'frank')
        self.assertEqual(myOptz.desc,         'frivolous')
        self.assertEqual(myOptz.epilog,        'fabulous')
        self.assertEqual(len(myOptz),          0)

    def testZOption(self):

        # booleans --------------------------------------------------

        bDfltVal    = True
        bDesc       = "I'm small"
        boolOpt     = BoolOption('bO', default=bDfltVal, desc=bDesc)
        self.assertEqual(boolOpt.name,          'bO')
        self.assertEqual(boolOpt.default,       bDfltVal)
        self.assertEqual(boolOpt.desc,          bDesc)

        # choice lists ----------------------------------------------

        # XXX We should probably require that list elements be of 
        # compatible types.  For the moment we just assume that elements
        # are all strings.
        
        # succeeds if default in list of choices ----------
        mySize      = 2 + self.rng.nextInt16(4)     # so in [2..5]
        choice      = self.rng.nextFileName(8)
        choices     = [choice]

        while len(choices) < mySize:
            if not choice in choices:
                choices.append(choice)
            choice  = self.rng.nextFileName(8)

        cDfltVal    = choices[self.rng.nextInt16(mySize)]
        cDesc       = 'a list'
        choiceOpt   = ChoiceOption('cO', choices, cDfltVal, cDesc)
        self.assertEqual(choiceOpt.name,        'cO')
        self.assertEqual(choiceOpt.choices,     choices)
        self.assertEqual(choiceOpt.default,     cDfltVal)
        self.assertEqual(choiceOpt.desc,        "a list")

        # fails if default is NOT in list of choices ------
        mySize      = 2 + self.rng.nextInt16(4)     # so in [2..5]
        choice      = self.rng.nextFileName(8)
        bChoices    = [choice]

        while len(bChoices) < mySize:
            if not choice in bChoices:
                bChoices.append(choice)
            choice  = self.rng.nextFileName(8)

        dfltVal      = self.rng.nextFileName(8)
        while dfltVal in choices:
            dfltVal  = self.rng.nextFileName(8)

        try:
            badChoiceOpt = ChoiceOption('bO', choices, 
                            default=dfltVal, desc="a list")
            self.fail('successfully added default value not in list of choices')
        except:
            pass

        # floats ----------------------------------------------------

        fDfltVal    = self.rng.nextReal()
        floatOpt    = FloatOption('fO', default=fDfltVal, desc="bubbly")
        self.assertEqual(floatOpt.name,         'fO')
        self.assertEqual(floatOpt.default,      fDfltVal)
        self.assertEqual(floatOpt.desc,         "bubbly")

        # ints ------------------------------------------------------

        iDfltVal    = self.rng.nextInt32()
        intOpt      = IntOption('iO', default=iDfltVal, desc="discrete")
        self.assertEqual(intOpt.name,           'iO')
        self.assertEqual(intOpt.default,        iDfltVal)
        self.assertEqual(intOpt.desc,           "discrete")

        # lists -----------------------------------------------------

        sizeVal     = self.rng.nextInt16()
        if self.rng.nextBoolean():
            sizeVal = - sizeVal

        listOpt     = ListOption('lO', default=sizeVal, desc="chunky")
        self.assertEqual(listOpt.name,          'lO')
        self.assertEqual(listOpt.default,       sizeVal)
        self.assertEqual(listOpt.desc,          "chunky")

        sizeVal     = 0
        varListOpt  = ListOption('zO', default=sizeVal, desc="skinny")
        self.assertEqual(varListOpt.name,       'zO')
        self.assertEqual(varListOpt.default,    sizeVal)
        self.assertEqual(varListOpt.desc,       "skinny")

        # strings ---------------------------------------------------

        sDfltVal    = self.rng.nextFileName(12)
        strOpt      = StrOption('sO', default=sDfltVal, desc="wiggly")
        self.assertEqual(strOpt.name,           'sO')
        self.assertEqual(strOpt.default,        sDfltVal)
        self.assertEqual(strOpt.desc,           "wiggly")

        # populate an Optionz object --------------------------------

        zName   = self.rng.nextFileName(8)
        zDesc   = self.rng.nextFileName(64)
        zEpilog = self.rng.nextFileName(64)
       
        myOptz = Z(zName, zDesc, zEpilog)

        self.assertEqual(myOptz.name,          zName)
        self.assertEqual(myOptz.desc,          zDesc)
        self.assertEqual(myOptz.epilog,        zEpilog)
        self.assertEqual(len(myOptz),          0)

        #               name    valType     default    desc
        myOptz.addOption('b0',  Z.O_BOOL,   bDfltVal,  bDesc)
        self.assertEqual(len(myOptz), 1)

        #choiceOpt   = ChoiceOption('cO', choices, cDfltVal, cDesc) # model
        # myOptz.addOption('cO', choices, default=cDfltVal, cDesc)
        
        # XXX WORKING HERE

if __name__ == '__main__':
    unittest.main()
