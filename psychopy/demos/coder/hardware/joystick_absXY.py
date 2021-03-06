#!/usr/bin/env python
from psychopy import *

#create a window to draw in
myWin = visual.Window((800.0,800.0), allowGUI=False)

if event.joystick.get_count()>0:
    myJoystick = event.Joystick(0)
    myJoystick.init()
    print 'found ', myJoystick.get_name(), ' with:'
    print '...', myJoystick.get_numbuttons(), ' buttons'
    print '...', myJoystick.get_numhats(), ' hats'
    print '...', myJoystick.get_numaxes(), ' analogue axes'
else:
    print "You don't have a joystick connected!?"
    myWin.close()
    core.quit()

#INITIALISE SOME STIMULI
fixSpot = visual.PatchStim(myWin,tex="none", mask="gauss",pos=(0,0), size=(0.05,0.05),color='black')
grating = visual.PatchStim(myWin,pos=(0.5,0),
                    tex="sin",mask="gauss",
                    color=[1.0,0.5,-1.0],colorSpace='rgb',
                    size=(0.2,.2), sf=(2,0),
                    autoLog=False)#this stim changes too much for autologging to be useful
message = visual.TextStim(myWin,pos=(-0.95,-0.95),text='Hit Q to quit')
trialClock = core.Clock()
t = 0
while 1:    
    #handle events first
    if myJoystick.get_button(0):
        myWin.close()
        core.quit()

    #get joystick data
    xx = myJoystick.get_axis(0)*1.0
    yy = myJoystick.get_axis(1)*1.0
    sf = (1+myJoystick.get_axis(2))*5.0
    deltaOri = myJoystick.get_axis(3)*-5.0
    grating.setPos((xx, -yy))
    grating.setSF(sf)
    if abs(deltaOri)>2:
        grating.setOri(deltaOri,'+')
    
    t=trialClock.getTime()
    
    fixSpot.draw()
    
    grating.setPhase(t*2)#moving at 2 Hz
    grating.draw()
    
    message.draw()
    event.clearEvents()#need to do this every frame
    myWin.flip()#redraw the buffer