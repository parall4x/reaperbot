__author__ = 'parallax'

import sys
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor


class ReaperBot(irc.IRCClient):
    def __init__(self):
        self.auth_key = "1337"
        self.authenticated = False
        self.master = ""

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return

        command = msg.split(" ", 1)[0]
        if command == "auth":
            operand = msg.split(" ", 1)[1]
            if operand == self.auth_key:
                self.authenticated = True
                self.master = user
                print user + " is now master"
                self.msg(channel, "Yes, master?")
            return

        if not self.authenticated or user != self.master:
            print "User " + user
            print "Master " + self.master
            print self.authenticated

            return

        self.msg(channel, "That's so interesting master, tell me more")





class BotFactory(protocol.ClientFactory):
    protocol = ReaperBot

    def __init__(self, channel, nickname='reaperbot'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
    chan = sys.argv[1]
    reactor.connectTCP('irc.oftc.net', 6667, BotFactory('#' + chan))
    reactor.run()