#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Main test driver for elopy, print touch events on terminal

Copyright 2015 Jonas Hauquier
Distributed under the terms of the GNU General Public License (GPL version 3 or any later version).
"""

import elopy
import yaml
import signal


def main(visualize=False):
    config = yaml.load(open('default_touch.yaml', 'r'))
    touch = elopy.Touch(dconfig=config['touch.hw.elo.Touch'])
    try:
        display = Display()
    except:
        print "pygame is not installed, guessing 640x480 as screen resolution"
        display = FakeDisplay()
    print "Display resolution: ", display.getPixelResolution()
    touch.setDisplay(display)

    if visualize:
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

    # Constantly get Touch events and update the position with the latest 
    # Touch event position. End demo when a
    # key event is received.
    last_position = touch._position
    run_demo=True
    while run_demo:
        if visualize:
            run_demo = display.pollWindowEvent()
        touch._poll()
        if touch._position != last_position:
            print 'Position: %s' % (touch._position, )
            last_position = touch._position
            if visualize:
                screen.drawPosition(last_position)

    print 'all done'


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


class FakeDisplay(Display):
    def getPixelResolution(self):
        # Return a fixed VGA resolution when we don't have pygame available to query the display resolution
        return [640, 480]

    def openFullscreenWindow(self):
        raise NotImplementedError("You need pygame installed for this feature.")

    def pollWindowEvent(self):
        raise NotImplementedError("You need pygame installed for this feature.")

    def closeWindow(self):
        raise NotImplementedError("You need pygame installed for this feature.")


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


def signal_handler(signal, frame):
    import os
    os._exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
