"""This is a module created such that common functions do not have to be copied into each program, and any function improvements will extend to all programs calling these classes.
Created by Akos Szekely"""
import os, sys

if os.getcwd() == 'J:\mystuff':
    sys.path.append('J:\Python27')
    sys.path.append('J:\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg\psychopy\app')
    sys.path.append('J:\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg\psychopy')
    sys.path.append('J:\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg')
    sys.path.append('J:\Python27\Lib\site-packages')
    sys.path.append('J:\Python27\Lib')
elif os.getcwd() == 'C:\Documents and Settings\\fmriuser\My Documents\MohantyLab':
    sys.path.append('C:\Documents and Settings\\fmriuser\My Documents\MohantyLab\Python27')
    sys.path.append(
        'C:\Documents and Settings\\fmriuser\My Documents\MohantyLab\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg\psychopy\app')
    sys.path.append(
        'C:\Documents and Settings\\fmriuser\My Documents\MohantyLab\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg\psychopy')
    sys.path.append(
        'C:\Documents and Settings\\fmriuser\My Documents\MohantyLab\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg')
    sys.path.append('C:\Documents and Settings\\fmriuser\My Documents\MohantyLab\Python27\Lib\site-packages')
    sys.path.append('C:\Documents and Settings\\fmriuser\My Documents\MohantyLab\Python27\Lib')
    from psychopy import parallel
elif os.getcwd() == 'C:\Users\mohantylab\mystuff':
    sys.path.append('C:\Python27')
    sys.path.append('C:\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg\psychopy\app')
    sys.path.append('C:\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg\psychopy')
    sys.path.append('C:\Python27\Lib\site-packages\psychopy-1.74.03-py2.7.egg')
    sys.path.append('C:\Python27\Lib\site-packages')
    sys.path.append('C:\Python27\Lib')

else:
    pass

import glob, random, fnmatch, math
from psychopy import visual, core, event, parallel
from collections import deque
from scipy import stats
import pkg_resources


class Starters():
    """Contains functions usually found at the start of the program, primarily for making lists"""

    def __init__(self):
        """All classes need this function.  I'm too new to classes to really do much with it right now."""
        pass

    def Lazylister(self, start=1, end=2, repeats=1, quantity=1, L=False, shuffle=True,
                   NoRepeats=False):  # if you need a repetitive list, use this
        """A favorite of mine, makes lists in a useful manner, requiring less input.  You want a list from 1-10?
        The first two inputs are 1 and 10.  You want a list from 1-10 with two of each element?  The next input is 2.
        You want three of those lists shuffled and put together?  The next input is 3.
        With this you can use .pop() to, say, show images 1-15 in a random order five times over,
        no images repeating until all images have been shown once."""
        if isinstance(L,
                      list):  # if you want a non-consecuitve list, or want a list of strings, you'll have to add that in to L directly as a list
            numbers = L  # we'll use that list
        else:
            numbers = [num for num in range(start,
                                            end + 1)]  # this list makes it so you don't have to type in all the numbers you want shuffled and combined
        Laziness = []  # empty lists are needed
        for repetition in range(0, repeats):  # repeat as many times as you must
            temp = []  # create an empty list.  This will contain the base unit of your larger list.
            for number in numbers:  # for the numbers present in numbers
                for x in range(0, quantity):  # quantity many times
                    temp.append(number)  # add each number to the empty list
            if shuffle:  # shuffle is True unless otherwise specified, so all these lists will be random before being combined with one another
                random.shuffle(temp)
                if NoRepeats:  # this one is a variable that defaults to False, but makes certain that none of the core elements repeat when combined with one another
                    if repetition > 0:  # you must be combining more than one core unit, otherwise there's no way of repeating anyway
                        while Laziness[-1] == temp[
                            0]:  # if the last element of the greater list is equal to the first element of the next core unit added in
                            random.shuffle(
                                temp)  # reshuffle the core unit.  Continue to do so until the two do not match
            else:  # if we aren't shuffling
                pass  # do nothing
            for item in temp:  # adds each item in the list just made to the whole list
                Laziness.append(item)
        return Laziness  # produce a list that is in order, contains the numbers you want in the quantities you want, just don't get repetitions mixed up with quantity of numbers

    def GlobOPics(self, path, picType, window=None, Size=None, Position=[0,0]):  # used to obtain all pictures beginning with a certain path and append them to a list for later use.
        """Takes the idea that you have images named something akin to "F1.jpg, F2.jpg, F3.jpg..." and runs with it.
        In path you write the path to the directory with the images, with a \F or whatever at the end.
        In picType you add '.jpg' for jpegs and so on. The Size and Position are variables that can be
        altered to suit your purposes, but by default are the natural image size and the center of the screen.
        This function then fills a list with psychopy ImageStims of all those images, using the psychopy visual.Window
        given by the window argument. Feel free to alter the window, image function, and so on."""
        List = []  # You don't have to make empty lists for this function to fill in the script itself
        stims = glob.glob(
            path + '*' + picType)  # basically this searches for anything starting with the path and ending in the picType.  While it's possible to specify a path as part of this function, it removes the location flexibility.
        PsychoPyVersion = pkg_resources.get_distribution("psychopy").version
        if float(PsychoPyVersion[0:4]) >= 1.75:
            for stim in stims:  # for all the files found
                List.append(visual.ImageStim(window, image=stim, mask=None, pos=Position,
                                             size=Size))  # add to the list the ImageStim object, meaning it can be drawn and we don't have to do this within any other function.
        else:
            for stim in stims:  # for all the files found
                List.append(visual.PatchStim(window, tex=stim, mask=None, pos=Position,
                                             size=Size))  # add to the list the PatchStim object, meaning it can be drawn and we don't have to do this within any other function.
        return List

    def SimGlP(self, path, picType, window=None, Position=[0,
                                                           0]):  # used to obtain all pictures beginning with a certain path and append them to a list for later use.
        """Takes the idea that you have images named something akin to "F1.jpg, F2.jpg, F3.jpg..." and runs with it.  In path you write the path to the directory with the images, with a \F or whatever at the end.  In picType you add '.jpg' for jpegs and so on.
        The Size and Position are variables that can be altered to suit your purposes, but by default are the natural image size and the center of the screen.  This function then fills a list with psychopy ImageStims of all those images, using the psychopy visual.Window given by the window argument.
        Feel free to alter the window, image function, and so on."""
        List = []  # You don't have to make empty lists for this function to fill in the script itself
        stims = glob.glob(
            path + '*' + picType)  # basically this searches for anything starting with the path and ending in the picType.  While it's possible to specify a path as part of this function, it removes the location flexibility.
        PsychoPyVersion = pkg_resources.get_distribution("psychopy").version
        if float(PsychoPyVersion[0:4]) >= 1.75:
            for stim in stims:  # for all the files found
                List.append(visual.SimpleImageStim(window, image=stim,
                                                   pos=Position))  # add to the list the ImageStim object, meaning it can be drawn and we don't have to do this within any other function.
        else:
            for stim in stims:  # for all the files found
                List.append(visual.PatchStim(window, tex=stim,
                                             pos=Position))  # add to the list the PatchStim object, meaning it can be drawn and we don't have to do this within any other function.
        return List

    def PatchGlob(self, path, picType, window=None, Size=None, Position=[0,
                                                                         0]):  # used to obtain all pictures beginning with a certain path and append them to a list for later use.
        """Takes the idea that you have images named something akin to "F1.jpg, F2.jpg, F3.jpg..." and runs with it.  In path you write the path to the directory with the images, with a \F or whatever at the end.  In picType you add '.jpg' for jpegs and so on.
        The Size and Position are variables that can be altered to suit your purposes, but by default are the natural image size and the center of the screen.  This function then fills a list with psychopy ImageStims of all those images, using the psychopy visual.Window given by the window argument.
        Feel free to alter the window, image function, and so on."""
        List = []  # You don't have to make empty lists for this function to fill in the script itself
        stims = glob.glob(
            path + '*' + picType)  # basically this searches for anything starting with the path and ending in the picType.  While it's possible to specify a path as part of this function, it removes the location flexibility.
        for stim in stims:  # for all the files found
            List.append(visual.PatchStim(window, tex=stim, mask=None, pos=Position,
                                         size=Size))  # add to the list the PatchStim object, meaning it can be drawn and we don't have to do this within any other function.
        return List

    def locate(self, pattern,
               root=os.curdir):  # this is taken from the internet.  Basically it says "okay, starting from where we are now, look for anything matching that pattern given.  You can therefore tweak its use by specifying the directory precisely.
        '''Locate all files matching supplied filename pattern in and below
        supplied root directory.'''
        for path, dirs, files in os.walk(os.path.abspath(
                root)):  # the abspath returns the absolute path of the current directory, the walk goes down the tree and spits out everything it finds.  Think of it as water trickling down cracks stemming from one point
            for filename in fnmatch.filter(files,
                                           pattern):  # looks in the files returned for those that match the pattern given when the function is called
                yield os.path.join(path,
                                   filename)  # basically this concatenates the path to the file and the filename itself.  Yield is complicated, but suffice to say it's a memory-efficient way of spitting out what we get as an object and forgetting it.

    def WaitTRPulse(self, location=None, numberPulses=1, ExperimentalClock=core.Clock(), Block_based_clock=core.Clock(),
                    window=None):  # waits for a TR pulse.  Should there be no need for that, just sets the time of the block start and moves right along
        """This uses several psychopy functions to read the TR pulses sent by an fMRI magnet.  It puts up a screen reading "waiting for scanner" until it gets the required number of pulses, indicated by numberPulses, which defaults to 1.
        It also indicates when the pulse was received according to a psychopy core.Clock that should be started at the beginning of the experiment and otherwise left unchanged (Allclock), and resets a psychopy core.Clock that should be
        reset once at the start of every block of the experiment (block/event related experiment, Scanclock).
        (e.g., WaitTRPulse('scan center',3); will wait for three TR pulses.)
        The location argument is a somewhat limited way to allow for testing this function outside of an fMRI environment.  If you type in 'scan center' it will attempt to use psychopy parallel functions, otherwise it'll default to psychopy's core.wait for numberPulses seconds.
        The win argument is how the "waiting for scanner" slide is presented.  It requires the psychopy visual module."""
        if location in ['scan center',
                        'scan centerP']:  # this means that only in one case will this function attempt to use parallel functions to get TR pulses
            Set8 = visual.TextStim(window, text='Waiting for the scanner', pos=[0, 0], color=(1.0, 1.0, 1.0),
                                   colorSpace='rgb', opacity=1.0, height=1.5, alignHoriz='center',
                                   wrapWidth=30)  # this is the image that will show up until the number of pulses has happened
            try:  # attempts to do these things, should an exception be reached does the stuff in except
                from psychopy import \
                    parallel  # if parallel isn't available a little thing will pop up in the output.  It's kind of annoying, so simply it's attempted and if failed moves on to the exception state
                Set8.draw()  # we show the slide telling the participant that we await the scanner's input
                window.flip()  # and make it visible
                for i in range(numberPulses):  # simple enough
                    while 1:  # why this of all things works best, I honestly don't understand.  In any case, it's a while loop that is only broken when it receives the parallel port information indicating that a pulse has been sent
                        if int(parallel.readPin(
                                15)):  # in the Stony Brook scan center the parallel input is from port 15
                            break  # breaks out of the while loop
                    pause = .1  # define how long we'll wait
                    core.wait(pause, hogCPUperiod=pause)  # and wait.  Also hogs the CPU, so nothing else happens
                    Pulse_on = ExperimentalClock.getTime()  # this is based on psychopy's event module and gets a time based on a core.Clock() hopefully made at the start of the experiment
            except:  # should there be no way to import parallel functions
                core.wait(numberPulses)  # just wait for however many seconds
                Pulse_on = ExperimentalClock.getTime()  # and indicate when the pulse should have been received
        else:  # behaviorally we do not wait, as there is no reason to
            Pulse_on = ExperimentalClock.getTime()  # we just get the time
        Block_based_clock.reset()  # at the end of any of these we reset the clock meant to indicate the events occuring within a block
        return Pulse_on

    def jitterprep(self, start, end, howmany, quantity, shuffle=True):  # troubles start at 9
        """In fMRI analysis you are dealing with the BOLD response, which takes 5 seconds to peak and near 20 to return to normal.  This means that unless you want to wait 20 seconds after every single trial, you need a different method.
        What you do is have each event happening at slightly different times, so the BOLD response peaks in different places.  The peaks all come together to form kind of a squiggly line.  If you have the times of all the events and the lengths of time
        they were up for, you can distinguish the peaks in the squiggly line and tell exactly what event they correspond to.  Hence, the jitter.  You start with a small number, say 3 seconds.  This is usually the length of a fixation cross up immediately
        after an event, such as showing a face.  You consider the number of trials you have a in a block, let's say 20.  Half that number will now be 3 seconds, so 10 trials will have a fixation up for 3 seconds.  Then you move to 4 seconds.  Half of the previous
        number will be 4, so there will be 5 trials of 4 seconds fixation.  Then halve that, so 2.5 trials of 5 seconds.  Then 1.25 of 6.  And so on.  Now, fractions of trials don't work.  So you have to jiggle things a bit so they fit.

        The way this function works:
            You put in the number you're starting with (say 3) and the number you're ending with (say 7).  Now, how many numbers do you want between those two.  This allows for fractions of seconds, which works a whole lot better than fractions of trials.
            Then, how many trials do you want in a block.  If you want five lengths in 9 trials per block, things start going pear-shaped.  It determines how many trials will have each length, and creates a list accordingly.  Then it checks if all the numbers are
            present and accounted for.  """
        x = round(start, 10)  # x will need to change, and also interact with float (decimal point) numbers
        increment = (((end + 1) - start) / float(
            howmany))  # the increments that will be used depends on how much distance must be covered, divided by how many units are desired
        listname = []  # always necessary
        temp = deque([])  # have to make a first-in-first-out list, despite it taking longer
        t = int(round(quantity * 0.5))  # again, quantity is fixed, so you need a variable
        temp.append(t)  # half the numbers will be of the first type
        u = t  # I don't know why this was necessary, only that things went wrong if I used t
        for v in range(0, howmany - 1):  # remember, you've already made the first number
            u = int(round(u * 0.5))  # halve the half, then halve that, and so on
            temp.append(u)  # and add it to the list
        if sum(
                temp) < quantity:  # now we get into the unpleasant stuff.  If all the numbers in the list don't add up to the quantity we need
            temp[-1] = temp[-1] + (quantity - sum(temp))  # add as many to the last number as we need.  Usually only 1.
        elif sum(
                temp) > quantity:  # the worst part.  If the sum of the numbers in the list is greater than the quantity we need, we have to start subtracting, but subtracting in such a way as to keep the proportion as clean as possible.
            problem = sum(
                temp) - quantity  # because it's a problem.  Seriously, try to make lists bigger than 9 in length.  Can't you just double the list and split it or something?
            temporary = list(
                temp)  # we're making a copy of the list, since we only want to alter the original list when everything's finished
            if problem == 1:  # so let's say we're one over
                a = temporary.index(2)  # find me the position of a 2, usually at the end
                temporary[a] = 1  # change that to a one.  Yay, easy and done
            elif problem == 2:  # okay, we're two over...
                a = temporary.index(2)  # same as before
                temporary[
                    a] = 1  # except that we have one left to subtract, and can't have any of the numbers in the list be 0.  Okay...
                try:  # let's give this a shot
                    b = temporary.index(3)  # find me the position of a three
                    temporary[b] = 2  # change it to a 2.  Yay, it worked!
                except:  # there are no threes.  Well,
                    b = temporary.index(4)  # find me the position of a four
                    temporary[b] = 3  # make it a three.  This is generally enough for lists longer than 9
            elif problem == 3:  # we're three over.  Crud
                a = temporary.index(2)  # same as before
                temporary[a] = 1
                try:
                    b = temporary.index(3)  # we'll do this the same way as before, except subtracting two
                    temporary[b] = 1
                except:
                    b = temporary.index(
                        4)  # if you want to refine this further, keep in mind that you'll start having to modify the first number, which could be 5.  You're going to have to make this line start another try-except loop
                    temporary[b] = 2
            temp = deque(temporary)  # okay, once it's all fixed, make the original the same as the copy
        else:  # no problems, move on
            pass
        for thing in range(0, howmany):  # for however many you're working on
            y = temp.popleft()  # take the leftmost number of the list
            for z in range(y):  # whatever that number is, that many times
                listname.append(x)  # add x to the list, which, remember, is initially equal to the starting value
            x += increment  # and we're adding the increment to it.  With all these decimals, some of the problems from before may be omitted.
        if end not in listname:  # for some reason the last number you wanted isn't part of your list.
            listname[-1] = end  # make it the absolute last number
        else:
            pass
        if shuffle:
            random.shuffle(listname)  # shuffle the list.  Saves you having to do it within the program
        else:
            pass
        return listname  # functions, this is how they work

    def find_repeats(self, L, contains, position, num_repeats, stop_after_match=False):
        """This function loops through a list of strings and checks if each """
        idx = 0
        valid = 0
        A = [item for item in L if item[position] == contains]
        while idx < len(L):
            for x in range(0, (len(A) - int(num_repeats))):
                if A[x:x + num_repeats] == L[idx:idx + num_repeats]:
                    L[idx:idx + num_repeats] = ['True'] * num_repeats
                    idx += num_repeats
                    if stop_after_match:
                        break
                        break
                else:
                    pass
            idx += 1
        if 'True' in L:
            valid = 0
        else:
            valid = 1
        return valid

    def OrderContingency(self, what_list, num_repeats, contains,
                         positions):  # uses find_repeats on all items in the list contains for all the positions in the list positions.  WARNING: doing this on a very large list is very likely to end in an infinite (or far too long) while loop.
        """5/31/12 this was modified to allow flexibility.  It's set up now that it'll look for the items in contains in each position in positions.  You can put all possibilities in contains and positions without a problem, this function will check all of them.
        As is, this will look for a set of things at several positions in a string within a list of strings.  Remember, this shuffles and spits out a list at the end, so it can't check a list without changing it.  You can modify this.
        6/8/12 modified the check portion of function to modify randomized copy rather than original.  Kinda stupid of me to have forgotten. -AS"""
        bool = 0  # get ready for a long while loop, with only one way out
        while bool == 0:
            # MAKE LIST COPY, SHUFFLE, PERFORM FUNCTIONS ON IT
            x = list(
                what_list)  # in order for this to work, we can't just continuously change one list, otherwise it fills up with 'True' strings and never ends.  So, we make a copy this way, such that the copy can be changed and re-copied without changing the original
            random.shuffle(x)  # shuffle the copy, doesn't touch original
            Validity = []  # instead of making a godawful number of find_repeats checks, we're just going to append the results of each check to this list
            if isinstance(positions, int):
                test = []
                for item in x:
                    test.append(item)
                for thing in contains:  # still English, but these two put together will look at all the items in contains at each point in the string specified in positions.
                    check = self.find_repeats(test, thing, 0, num_repeats,
                                              True)  # use the find_repeats function and get either a 1 or a 0 out of it
                    Validity.append(check)  # add that to Validity
            for position in positions:  # this one makes sense in English
                test = []
                for item in x:
                    y = item.split('*')
                    test.append(y[position])
                for thing in contains:  # still English, but these two put together will look at all the items in contains at each point in the string specified in positions.
                    check = self.find_repeats(test, thing, 0, num_repeats,
                                              True)  # use the find_repeats function and get either a 1 or a 0 out of it
                    Validity.append(check)  # add that to Validity
                    # DEAL WITH FUNCTION RESULT
            if Validity == [1] * len(
                    Validity):  # basically if Validity is equal to a list of just 1s as long as Validity is
                bool = 1  # while loop ends
                what_list = x  # the copy takes the place of the original as a properly shuffled list with no unseemly amounts of repetition
            else:
                pass
        return what_list  # nice and clean result.  If you want to only check things without altering the original list, comment out what_list=x and have this function return x instead.

    def BusyWaiting(self, timer,
                    timeout=False):  # a basic while loop for an amount of time that lets you quit and nothing else.
        event.clearEvents()  # sometimes having pressed a button earlier carries over, so best to have this be a part of getting the keys
        if timeout:
            if isinstance(timeout, str):
                for frame in range(int(timeout)):
                    for key in event.getKeys():  # this allows the last button pressed to be what's returned.  Unless pressing a button allows you to quit immediately
                        if key in ['q', 'escape']:  # like pressing q or the escape key does
                            return 0
                        elif key == 'num_multiply':
                            return 2
            else:
                timer.reset()  # reset the timer before the loop
                while timer.getTime() < timeout:  # while the time hasn't run out
                    for key in event.getKeys():  # this allows the last button pressed to be what's returned.  Unless pressing a button allows you to quit immediately
                        if key in ['q', 'escape']:  # like pressing q or the escape key does
                            return 0
                        elif key == 'num_multiply':
                            return 2
        else:
            for key in event.waitKeys():
                if key in ['q', 'escape']:
                    return 0
                elif key == 'num_multiply':
                    return 2
        return 1

    def TrialFeedback(self, Feedback, timer=False, window=None, dataFile=False):
        Feedback_Dictionary = {}
        try:
            Feedback_Dictionary[1] = visual.TextStim(window, text='CORRECT', pos=[0, 0], color=('black'),
                                                     colorSpace='rgb', opacity=1.0, height=1, alignHoriz='center',
                                                     wrapWidth=40)
            Feedback_Dictionary[0] = visual.TextStim(window, text='INCORRECT', pos=[0, 0], color=('black'),
                                                     colorSpace='rgb', opacity=1.0, height=1, alignHoriz='center',
                                                     wrapWidth=40)
            Feedback_Dictionary[Feedback].draw()
            window.flip()
        except:
            print 'window must be a Psychopy visual.Window object'
            core.quit()
        if timer:
            QuitNum = self.BusyWaiting(timer, 2)
        else:
            QuitNum = self.BusyWaiting(0)
        if QuitNum == 0:
            if dataFile:
                dataFile.close()
            else:
                pass
            core.quit()
        else:
            pass

    def FindPictures(self, PicList=False, Directory=False):
        for x in range(0, len(os.path.dirname(os.getcwd()).split('\\'))):
            PathToAllPicturesYouWant = 'N/A'
            for path, dirs, files in os.walk(os.getcwd()):
                if PicList:
                    if set(PicList).issubset(files):
                        PathToAllPicturesYouWant = path
                if Directory:
                    if Directory in dirs:
                        PathToAllPicturesYouWant = os.path.join(path, Directory)
            if PathToAllPicturesYouWant == 'N/A':
                os.chdir(os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..')))
            else:
                break
        return PathToAllPicturesYouWant

    def Frange(self, e, s=0.0, i=1.0):
        """A type of replacement for the range function, allows float steps.
        Due to the way the variables are set up, you need to enter the starting value after the ending value."""
        L = []
        while s + i <= e:
            L.append(s)
            if s == e:
                break
            elif s + i >= e:
                break
            else:
                pass
            s += i
        return L

    def Separator(self, total, length):
        out = []
        if length % 2 == 0:
            for x in range(length / 2):
                halved = total / (2 * (x + 1))
                out.append(halved)
                out.append(-1 * halved)
        else:
            for x in range(length / 2):
                halved = total / (2 * (x + 1))
                out.append(halved)
                out.append(-1 * halved)
            out.append(0)
        random.shuffle(out)
        return out


class Enders():
    """Contains functions usually found toward the end of a program, primarily for data analysis."""

    def __init__(self):
        """All classes need this function.  I'm too new to classes to really do much with it right now."""
        pass

    def PsychophysicsDictMaker(self, Conditions, Secondary=None, Tertiary=None, Quarternary=None, five=None):
        PsychophysicsDict = {}
        for condition in Conditions:
            PsychophysicsDict['dResponses' + condition] = []
            for type in ['Acc', 'AvgRT']:
                PsychophysicsDict[condition + type] = []
                try:
                    for second in Secondary:
                        PsychophysicsDict[second + condition + type] = []
                        PsychophysicsDict[second + type] = []
                        PsychophysicsDict['dResponses' + second + condition] = []
                        PsychophysicsDict['dResponses' + second] = []
                        try:
                            for third in Tertiary:
                                PsychophysicsDict[second + third + condition + type] = []
                                PsychophysicsDict[second + third + type] = []
                                PsychophysicsDict[third + condition + type] = []
                                PsychophysicsDict[third + second + type] = []
                                PsychophysicsDict['dResponses' + third + condition] = []
                                try:
                                    for fourth in Quarternary:
                                        PsychophysicsDict[second + third + fourth + condition + type] = []
                                        PsychophysicsDict[third + fourth + condition + type] = []
                                        PsychophysicsDict[second + fourth + condition + type] = []
                                        PsychophysicsDict[fourth + condition + type] = []
                                        try:
                                            for fifth in five:
                                                PsychophysicsDict[
                                                    second + third + fourth + fifth + condition + type] = []
                                                PsychophysicsDict[second + third + fifth + condition + type] = []
                                                PsychophysicsDict[third + fourth + fifth + condition + type] = []
                                                PsychophysicsDict[second + fourth + fifth + condition + type] = []
                                                PsychophysicsDict[fourth + fifth + condition + type] = []
                                                PsychophysicsDict[fifth + condition + type] = []
                                        except:
                                            pass
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
                    #        return Conditions,Secondary,Tertiary,Quarternary,five,PsychophysicsDict
        return PsychophysicsDict

    def Average(self, respList, type=False, Input=False,
                File=False):  # for calculating average (accuracy or rt) given a bunch of responses
        total = 0.0  # start from scratch, and make it a float number so you don't get a bunch of 0s.
        # ADD REACTION TIMES TOGETHER
        for item in respList:  # read every time in the list until the end
            if isinstance(item, str):  # redundancy is useful.  This removes any string from the reaction times list
                respList.remove(item)
            else:  # so if it's not a string
                total += item  # add the time to total
                # DIVIDE BY AMOUNT OF REACTION TIMES
        try:
            Average = float(total) / len(
                respList)  # divide the sum of rts by the amount of rts (that's why we had to remove the strings from the list, so as to not bias this calculation)
        except ZeroDivisionError:  # your list has no items in it
            Average = 'N/A'  # average is marked as 0, so you have something
            # WRITING IT
        if File:
            if Input:
                File.write('"Average %s %s:",%s,\n' % (Input, type, Averag))
            else:
                File.write('"Average %s:",%s,\n' % (type,
                                                    Average))  # SMG -- changed PARENTHESES to BRACKETS to try and fix tuple error, but this was unsuccessful.
        else:
            return Average

    def HitRate(self, Responses, Input=False, File=False):  # this works to determine hit rate and print it
        """Functionally, this counts the amount of strings reading 'Hit' and the number of strings reading 'Miss' in a list.  Then averages them as if Hit is 1 and Miss is 0.  There are options for dealing with no hits or misses, all hits, or all misses.  None of these are
        acceptable for perceptual sensitivity analyses.  The options for the latter two conditions (all hits or misses) are taken from a website (http://www.linguistics.ucla.edu/faciliti/facilities/statistics/dprime.htm) and are considered standard."""
        try:  # this is set up to deal with a specific issue, namely dividing by zero when there are too many non-responses
            HitRate = round(Responses.count('Hit'), 10) / (Responses.count('Hit') + Responses.count(
                'Miss'))  # generally it's just hits divided by hits and misses, with rounding to make sure it's a float number and doesn't result in just 0s
        except ZeroDivisionError:  # but with enough non-responses
            HitRate = 1.000 / 102  # we'll just make it equal to the standard way of dealing with a 0
        if HitRate == 1:  # if they got all hits
            HitRate = 101.00 / 102  # we use this approach to have a workable number for d', as 1 and 0 cause failures.  Google d prime for more information
        elif HitRate == 0:  # if they got all misses
            HitRate = 1.000 / 102  # another standard way of dealing with a 1 or 0.
        else:  # no problems = no changes
            pass
        if File:
            File.write('"Hit Rate %s:",%s,\n' % (Input, HitRate))  # write on the data file
        return HitRate

    def FArate(self, Responses, Input=False,
               File=False):  # this determines false alarm rate and is basically the same thing as the HitRate function
        """Functionally, this counts the amount of strings reading 'False Alarm' and the number of strings reading 'Correct Rejection' in a list.  Then averages them as if False Alarm is 1 and Correct Rejection is 0.  There are options for dealing with no hits or misses, all hits, or all misses.  None of these are
        acceptable for perceptual sensitivity analyses.  The options for the latter two conditions (all FAs or CRs) are taken from a website (http://www.linguistics.ucla.edu/faciliti/facilities/statistics/dprime.htm) and are considered standard."""
        try:  # seriously, it's the exact same function with different names
            FArate = round(Responses.count('False Alarm'), 10) / (
            Responses.count('False Alarm') + Responses.count('Correct Rejection'))
        except ZeroDivisionError:
            FArate = 101.00 / 102
        if FArate == 0.00:
            FArate = 1.000 / 102
        elif FArate == 1.00:
            FArate = 101.00 / 102
        else:
            pass
        if File:
            File.write('"False Alarm Rate %s:",%s,\n' % (Input, FArate))
        return FArate

    def CRrate(self, Responses, Input=False,
               File=False):  # this determines correct rejection rate/specificity and is basically the same thing as the HitRate function
        """Functionally, this counts the amount of strings reading 'Correct Rejection' and the number of strings reading 'False Alarm' in a list.  Then averages them as if False Alarm is 0 and Correct Rejection is 1.  There are options for dealing with no hits or misses, all hits, or all misses.  None of these are
        acceptable for perceptual sensitivity analyses.  The options for the latter two conditions (all FAs or CRs) are taken from a website (http://www.linguistics.ucla.edu/faciliti/facilities/statistics/dprime.htm) and are considered standard."""
        try:  # seriously, it's the exact same function with different names
            CRrate = round(Responses.count('Correct Rejection'), 10) / (
            Responses.count('False Alarm') + Responses.count('Correct Rejection'))
        except ZeroDivisionError:
            CRrate = 101.00 / 102
        if CRrate == 0.00:
            CRrate = 1.000 / 102
        elif CRrate == 1.00:
            CRrate = 101.00 / 102
        else:
            pass
        if File:
            File.write('"Correct Rejection Rate (Specificity) %s:",%s,\n' % (Input, CRrate))
        return CRrate

    def PPV(self, Responses, Input=False,
            File=False):  # this determines correct rejection rate/specificity and is basically the same thing as the HitRate function
        """Functionally, this counts the amount of strings reading 'Hit' and the number of strings reading 'False Alarm' in a list.  Then averages them as if False Alarm is 0 and Hit is 1.  There are options for dealing with no hits or misses, all hits, or all misses.  None of these are
        acceptable for perceptual sensitivity analyses.  The options for the latter two conditions (all FAs or Hits) are taken from a website (http://www.linguistics.ucla.edu/faciliti/facilities/statistics/dprime.htm) and are considered standard."""
        try:  # seriously, it's the exact same function with different names
            PPV = round(Responses.count('Hit'), 10) / (Responses.count('False Alarm') + Responses.count('Hit'))
        except ZeroDivisionError:
            PPV = 101.00 / 102
        if PPV == 0.00:
            PPV = 1.000 / 102
        elif PPV == 1.00:
            PPV = 101.00 / 102
        else:
            pass
        if File:
            File.write('"Positive Predictive Value %s:",%s,\n' % (Input, PPV))
        return PPV

    def Zscore(self, Rate, type=False, Input=False,
               File=False):  # this calculates the Zscore of a given rate or really any decimal between 0 and 1.
        """This function uses scipy's stats class and the norm.ppf function in that on any given rate to determine a z score.  This was determined by comparing Excel's NORM.INV function output to several norm function outputs in scipy.
        Turns out NORM.S.INV results in the same thing as NORM.INV with a mean of 0 and a std dev of 1, so even though the former should have been used for comparison, they result in the same thing."""
        if Rate == 0.00:  # redundancy is useful at times
            Rate = (1.000 / 102)  # standard method
        elif Rate == 1.00:
            Rate = 101.00 / 102
        else:
            pass
        Z = stats.norm.ppf(
            Rate)  # this is how we calculate a Z score.  It uses the stats class, and the norm.ppf function.  Look up the class if you wish, the function has been tested against other methods and gives the correct response
        if File:
            File.write('"Z %s %s:",%s,\n' % (type, Input, Z))  # write the Z score.
        return Z

    def dPrime(self, ZHit, ZFA, Input=False, File=False):  # calculates d' from the proper two Z scores
        """This subtracts two z scores.  To be honest, it just subtracts any two numbers that you give it."""
        d = ZHit - ZFA  # this is the formula
        if File:
            File.write('"d Prime %s:",%s,\n' % (Input, d))  # and it's written
        else:
            return d

    def Beta(self, ZHit, ZFA, Input=False, File=False):  # calculates beta from the proper two Z scores
        """This one is taken from another paper on signal detection theory (http://people.brandeis.edu/~sekuler/stanislawTodorov1999.pdf).  The use of math.exp was the result of a Google search for Excel's EXP function in python."""
        B = math.exp((ZFA ** 2 - ZHit ** 2) / 2)
        if File:
            File.write('"Beta %s:",%s,\n' % (Input, B))  # and it's written
        else:
            return B

    def ErrorPercent(self, respList, type=False, Input=False,
                     File=False):  # to calculate error percentage, given a list
        total = 0.0  # start from scratch, and make it a float number so you don't get a bunch of 0s.
        # ADD REACTION TIMES TOGETHER
        for item in respList:  # read every time in the list until the end
            if isinstance(item, str):  # redundancy is useful.  This removes any string from the reaction times list
                respList.remove(item)
            elif item == 0:  # so if it's not a string
                total += 1.0  # add the time to total
        try:
            ErrorPercent = float(total) / len(
                respList)  # divide the sum of rts by the amount of rts (that's why we had to remove the strings from the list, so as to not bias this calculation)
        except ZeroDivisionError:  # your list has no items in it
            ErrorPercent = 'N/A'  # average is marked as 0, so you have something
        if File:
            if Input:
                File.write('"Error Percent %s %s:",%s,\n' % (Input, type, ErrorPercent))
            else:
                File.write('"Error Percent %s:",%s,\n' % (type, ErrorPercent))
        else:
            return ErrorPercent

    def C_Calc(self, HitRate, FArate, Input=False, File=False):
        """Calculates the C statistic.  The stats.norm.ppf bit is equivalent to Excel's NORM.S.INV function.  See the Beta function for the paper where I got this calculation."""
        C = -(stats.norm.ppf(HitRate) + stats.norm.ppf(FArate)) / 2
        if File:
            File.write('"C %s:",%s,\n' % (Input, C))  # writes C
        else:
            return C

    def logBias(self, respList1, respList2, types=False, File=False):
        """Calculates a log of bias.  Taken from personal communication w/ Christian Luhman 4/4/2014"""
        logB = .5 * math.log10((respList1.count(1) * respList2.count(0)) / (respList1.count(0) * respList2.count(1)))
        if File:
            try:
                File.write('log bias %s vs %s:,%s,\n' % (types[0], types[1], logB))
            except:
                File.write('log bias unknown terms:,%s,\n' % (logB))


start = Starters()
end = Enders()