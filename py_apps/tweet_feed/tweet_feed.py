#-------------------------------------------------------------------------------
# Tweet Feed
#
# Author: Shawn Hymel @ SparkFun Electronics
# Date: April 14, 2014
# License: This code is beerware; if you see me (or any other SparkFun employee)
# at the local, and you've found our code helpful, please buy us a round!
# Distributed as-is; no warranty is given.
#
# Sets up a Twython listener object and queues up commands when a Tweet mentions
# @KilroyTheRobot.
#-------------------------------------------------------------------------------

import Queue
import threading
from twython import Twython, TwythonStreamer, TwythonError

#-------------------------------------------------------------------------------
# Class - TweetStreamer
#
# Waits for callbacks from Twitter API and puts commands seen into a queue
#-------------------------------------------------------------------------------

class TweetStreamer(TwythonStreamer):

    # [Constructor] Inherits a Twython streamer. Pass in queues.
    def __init__(self, parent, commands, app_key, app_secret, oauth_token, 
                    oauth_token_secret, debug=0, timeout=300, retry_count=None,
                    retry_in=10, client_args=None, handlers=None, chunk_size=1):
        TwythonStreamer.__init__(self, app_key, app_secret, oauth_token, 
                    oauth_token_secret, timeout=300, retry_count=None, 
                    retry_in=10, client_args=None, handlers=None, 
                    chunk_size=1)
        self.parent = parent
        self.cmd_list = commands
        self.debug = debug
    
    # Callback from streamer when robot's name appears in a Tweet. Fill queue.
    def on_success(self, data):
        if 'text' in data:
        
            # Add user to command list
            usr = data['user']['screen_name'].encode('utf-8')
            usr = '@' + usr
            self.parent.put_command(usr)
            
            # Extract commands from Tweet and place in queue
            msg = data['text'].encode('utf-8')
            words = msg.split(' ')
            cmds = [w for w in words if w in self.cmd_list]
            if self.debug > 0:
                print ''
                print msg
                print cmds
            for c in cmds:
                self.parent.put_command(c)
                
            
    # Callback from streamer if error occurs
    def on_error(self, status_code, data):
        print status_code, data
        
    # Called from main thread to stop the streamer
    def stop(self):
        self.disconnect()
        
#-------------------------------------------------------------------------------
# Class - TweetFeed
#
# Sets up a Twython streamer and provides access to Tweets and command queue
#-------------------------------------------------------------------------------

class TweetFeed:

    # [Constructor] Setup streamer thread
    def __init__(self, twitter_auth, debug=0):
    
        # Declare class members
        self.auth_args = None
        self.cmd_list = None
        self.cmd_queue = None
        self.debug = None
        self.thread_stream = None
        self.track_terms = None
        self.twitter = None
     
        # Set debug level
        self.debug = debug
        
        # Create command queue
        self.cmd_queue = Queue.Queue()
        
        # Extract authentication tokens
        app_key = twitter_auth['app_key']
        app_secret = twitter_auth['app_secret']
        oauth_token = twitter_auth['oauth_token']
        oauth_token_secret = twitter_auth['oauth_token_secret']
        self.auth_args = (  app_key, 
                            app_secret, 
                            oauth_token, 
                            oauth_token_secret)
                            
        # Setup Twitter object to send tweets
        self.twitter = Twython( app_key, 
                                app_secret, 
                                oauth_token, 
                                oauth_token_secret)
                                
    # [Private] Setup streamer and filter(s)
    def __create_twitter_streamer(  self, 
                                    app_key, 
                                    app_secret, 
                                    oauth_token, 
                                    oauth_token_secret ):
        self.track_stream = TweetStreamer(  self, 
                                            self.cmd_list,
                                            app_key, 
                                            app_secret,
                                            oauth_token,
                                            oauth_token_secret,
                                            self.debug)
        self.track_stream.statuses.filter(track=self.track_terms)
        
    # [Public] Start Twitter streamer
    def start_streamer(self, search_terms, commands):
    
        # Setup tracking terms and command list
        self.cmd_list = commands
        self.track_terms = search_terms
        
        # Start streamer inside thread
        self.thread_stream = threading.Thread( \
                target=self.__create_twitter_streamer, args=self.auth_args)
        self.thread_stream.daemon = True
        self.thread_stream.start()
        
    # [Public] Stop the streamer and wait for thread to end
    def stop_streamer(self, timeout=None):
        self.track_stream.stop()
        self.thread_stream.join(timeout)
        del self.thread_stream
        
    # [Public] Puts a command into the queue
    def put_command(self, cmd):
        self.cmd_queue.put(cmd)
        
    # [Public] Gets all commands from queue in a list
    def get_commands(self):
    
        commands = []
        
        #Add delimiter to the queue
        self.cmd_queue.put(-1)
        
        # Pull commands from queue and add to the list
        while not self.cmd_queue.empty():
            cmd = self.cmd_queue.get()
            if cmd == -1:
                break
            else:
                commands.append(cmd)
                
        return commands