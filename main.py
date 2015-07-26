#!/usr/bin/python2.7

##
# Main test driver for elopy
##

import elotouchdevice
import yaml

class Display(object):
    def __init__(self):
        import pygame
        pygame.display.init()

    def getPixelResolution(self):
        import pygame
        info = pygame.display.Info()
        return info.current_w, info.current_h

    def getCoordBounds(self):
        """
        Returns [left, top, right, bottom]
        """
        # TODO must come from calibration
        w,h = self.getPixelResolution()
        #return [0, 0, w, h]
        #return [4000, 90 , 0, 4000]
        return [0, 4000 , 4000, 90]

    def openFullscreenWindow(self):
        import pygame

        background_colour = (255,255,255)
        (width, height) = self.getPixelResolution()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Tutorial 1')
        screen.fill(background_colour)

        pygame.display.toggle_fullscreen()

        pygame.display.flip()
        return Screen(screen)

    def closeWindow(self):
        import pygame
        pygame.display.quit()
        pygame.quit()

    def pollWindowEvent(self):
        import pygame
        ev = pygame.event.poll()
        if ev == pygame.NOEVENT:
            return True
        if ev.type == pygame.QUIT:
            self.closeWindow()
            return False
        elif ev.type == pygame.KEYDOWN:
            '''
            if ev.key == pygame.K_ESCAPE:
                self.closeWindow()
                return False
            '''
            # Press any key to exit
            self.closeWindow()
            return False
        return True

class Screen(object):
    def __init__(self, pygamescreen):
        self.screen = pygamescreen

    def drawPosition(self, pos):
        import pygame
        x, y = pos
        self.screen.fill((255,255,255))
        radius = 10
        thickness = 2
        #print "Draw", x, y
        pygame.draw.circle(self.screen, (255,0,0), (int(x),int(y)), radius, thickness)
        pygame.display.update()

def main():
    config = yaml.load(open('default_touch.yaml', 'r'))
    #print config
    touch = elotouchdevice.Touch(dconfig=config['touch.hw.elo.Touch'])
    display = Display()
    print "Display resolution: ", display.getPixelResolution()
    touch.setDisplay(display)

    screen = display.openFullscreenWindow()

    # Issue a query on the ID settings and get the reply as a dict of 
    # parsed values. See the elo_serial.py in psychopy/iohub/devices/touch/hw/elo
    # to see what are valid query names. In the elo_serial.py a subset of
    # the classes are named Query*, where * is the query name. The query 
    # associated with any Query* class can be issued from a psychopy script 
    # by calling the following method of the touch device with the * part
    # of the Query class name:
    #
    #   # Issue an ID Query and get the response from the elo device.
    #   query_reply=touch.queryDevice('ID') 
    #   
    id_dict=touch.queryDevice('ID')
    print "queryDevice('ID'):",id_dict
    print
    
    # getHardwareConfiguration returns the results from the following 
    # queries, issued when the elo device interface was created by iohub:
    #
    #   ID
    #   Diagnostics
    #   Owner
    #   Jumper
    #   Report
    #
    hw_conf_dict=touch.getHardwareConfiguration()    
    import pprint
    print "hw_conf_dict:"
    pprint.pprint(hw_conf_dict)
    print

    
    # Clear all events from the global and device level event buffers.
    #self.hub.clearEvents('all') 
    touch.clearEvents()

    # TODO calibration
    '''
    # determine whether calibration has been enabled.
    user_params=self.getUserDefinedParameters()        
    #
    if user_params.get('calibrate_elo',False) is True:        
        #Calibrate
        self.run_elo_calibration()   
        self.hub.clearEvents('all')
        #Validate
        terminate_calibration=False
        while not terminate_calibration and self.run_elo_validation() is False:
            self.run_elo_calibration() 
            kb_events=kb.getEvents()
            if kb_events:
                terminate_calibration=True
            self.hub.clearEvents('all')

        # End demo if calibration has been cancelled.
        if terminate_calibration is True:
            return False
            
        #Save elo device settings to NVRAM
        self.touch.saveConfiguration()
    else:
        self.touch.restoreConfiguration()
    '''

    #self.hub.clearEvents('all')
    touch.clearEvents()
    
    # Constantly get Touch events and update the touch_contingent_stim
    # position with the latest Touch event position. End demo when a
    # key event is received.
    last_position = touch._position
    run_demo=True
    while run_demo:
        #touch_events=touch.getEvents()
        run_demo = display.pollWindowEvent()
        touch._poll()
        if True:  #touch_events:
            #te=touch_events[-1]
            #print te.x_position, te.y_position
            if touch._position != last_position:
                print 'Position: %s' % (touch._position, )
                last_position = touch._position
                screen.drawPosition(last_position)
            
    # DONE EXP

    print 'all done'


def run_elo_calibration(touch, display): 
    """
    Performs the Touch device Calibration routine. 
    Calibration is done using three sample points.
    """
    touch.initCalibration()

    display_resolution=display.getPixelResolution()
    xmin=0
    ymin=0
    xmax=display_resolution[0]
    ymax=display_resolution[1]
    dwidth=xmax
    dheight=ymax
    
    horz_margin=dwidth*.1
    vert_margin=dheight*.1
    
    leftx = xmin+horz_margin 
    uppery = ymin+vert_margin   
    rightx = xmax-horz_margin
    lowery = ymax-vert_margin

    print "Elo Touch Screen Calibration.\n \
Touch each Point when it is Presented."
            
    cal_points=[
                (leftx-dwidth/2, -(uppery-dheight/2)),
                (rightx-dwidth/2, -(lowery-dheight/2)),
                (rightx-dwidth/2, -(uppery-dheight/2))
                ]

    ts_points=[]
    
    for x,y in cal_points:
        ts_points.append(getTouchPoint(x,y))

    (x1,y1),(x2,y2),(sx,sy)=ts_points 

    touch.applyCalibrationData(xmin,xmax,ymin,ymax,
                                  x1,y1,x2,y2,sx,sy,
                                  leftx,uppery,rightx,lowery)

    self.cal_instruct_stim.setText('CALIBRATION COMPLETE.\nPRESS ANY KEY TO CONTINUE.')
    self.cal_instruct_stim.setPos((0,0))
    self.cal_instruct_stim.draw()
    self.window.flip()
    self.hub.clearEvents('all')
    kb=self.devices.kb
    while not kb.getEvents(EventConstants.KEYBOARD_PRESS):
       time.sleep(0.05)
    self.hub.clearEvents('all')

def getTouchPoint(x,y, touch):
    # Displays a target stim for calibration or validation. Returns
    # the location of the first Touch Release event received.
    '''
    self.touch_point_stim.pos=(x,y)
    self.touch_point_stim.draw()
    self.cal_instruct_stim.draw()
    self.window.flip()
    '''
    # TODO draw on screen
    
    touch.clearEvents()

    no_touch_release=True
    while no_touch_release:
        touch_events=touch.getEvents()
        for te in touch_events:                   
            if te.type==EventConstants.TOUCH_RELEASE:
                return te.x_position,te.y_position

        #not self.devices.kb.getEvents(event_type_id=EventConstants.KEYBOARD_PRESS):
        #self.touch_point_stim.draw()
        #self.cal_instruct_stim.draw()
        #self.window.flip()
        time.sleep(0.05)
    touch.clearEvents()


if __name__ == "__main__":
    main()
