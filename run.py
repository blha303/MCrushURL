import sys, unicodedata, yaml, PyCrush
from HTMLParser import HTMLParser
from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.web.client import getPage
from twisted.application import internet, service

with open('config.yml') as f:
    config = yaml.load(f.read())
HOST, PORT = config['host'], config['port']

class MediaCrushProtocol(irc.IRCClient):
    nickname = 'MCrushURL'
    username = 'MediaCrush'
    versionName = 'MediaCrush'
    versionNum = 'v1.0'
    realname = 'blha303'
 
    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
 
    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        print "<%s> %s" % (nick, message)
        if message.split(" ")[0] == "!url" and len(message.split(" ")) > 1 and "http" in message:
            print "Trying to send request"
            url = message[5:]
            mc = PyCrush.API()
            data = mc.upload_url(url=url)
            if "hash" in data[0]:
                self._send_message("https://mediacru.sh/" + data[0]["hash"].encode('ascii', 'ignore'), channel, nick=nick)
            else:
                errors = {409: "The file was already uploaded.",
                          420: "The rate limit was exceeded. Enhance your calm.",
                          415: "The file extension is not acceptable.",
                          404: "The destination URL was not found."}
                if data[1] in errors:
                    self._send_message(errors[data[1]], channel, nick=nick)

    def _send_message(self, msg, target, nick=None):
        if nick:
            msg = '%s, %s' % (nick, msg)
        print "<%s> %s" % (self.nickname, msg)
        self.msg(target, msg)
 
    def _show_error(self, failure):
        return failure.getErrorMessage()
 
class MediaCrushFactory(protocol.ReconnectingClientFactory):
    protocol = MediaCrushProtocol
    channels = config["channels"]
 
if __name__ == '__main__':
    reactor.connectTCP(HOST, PORT, MediaCrushFactory())
    log.startLogging(sys.stdout)
    reactor.run()
 
elif __name__ == '__builtin__':
    application = service.Application('MediaCrush')
    ircService = internet.TCPClient(HOST, PORT, MediaCrushFactory())
    ircService.setServiceParent(application)
