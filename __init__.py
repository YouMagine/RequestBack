# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from urllib2 import Request, urlopen, URLError
from urlparse import urlparse

class RequestBackPlugin(octoprint.plugin.StartupPlugin):  
    def on_after_startup(self):
        self._log("RequestBack is life!")
        # next line is for testing
        #self.custom_action_handler(24, "// action:http://tamara.nu", "http://tamara.nu")

    def get_update_information(self):
        # softwareupdate hook
        return dict(
            requestback=dict(
            displayName="RequestBack",
            displayVersion=self._plugin_version,
            #version check: github repository
            type="github_release",
            user="YouMagine",
            repo="RequestBack",
            current=self._plugin_version,
            # update method: pip
            pip="https://github.com/YouMagine/RequestBack/archive/{target}.zip"
            )
        )
    
    def _log(self, line):
        # easy editting for logging type
        self._logger.info(line)
    
    def add_action_comment(self):
        # This is the beginning of a preprocessor
        if not octoprint.filemanager.valid_file_type(path, type="gcode"):
            return file_object     
        
    def putRequest(self, url):
        request = Request(url)
        # There are also possibilities to add some data to the request
        # Like some data regarding the printer
        request.add_header('User-agent', 'Octoprint-RequestBack')
        request.get_method = lambda: 'PUT'
        try:
            response = urlopen(request)
        except URLError, e:
            if hasattr(e, 'reason'):
                self._log('We failed to reach a server.')
                self._log('Reason: %s' % e.reason)
            elif hasattr(e, 'code'):
                self._log('The server could not fulfill the request.')
                self._log('Error code: %s' % e.code)
        else:
            self._log('putrequest send to: %s' % url)
        
    def custom_action_handler(self, comm, line, action, *args, **kwargs):
        UrlValidator = urlparse(action)
        if UrlValidator.scheme != '' and UrlValidator.netloc != '':
            # The request URL is validated, so we can make a put request
            self.putRequest(action)
        else:
            self._log('The action is not an url: %s' % action)
        

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RequestBackPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        #"octoprint.filemanager.preprocessor": __plugin_implementation__.add_action_comment, 
        "octoprint.comm.protocol.action": __plugin_implementation__.custom_action_handler
    }

