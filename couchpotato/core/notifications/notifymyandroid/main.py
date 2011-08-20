from couchpotato.core.logger import CPLog
from couchpotato.core.notifications.base import Notification
from libs import pynma

log = CPLog(__name__)


class NotifyMyAndroid(Notification):

    listen_to = ['movie.downloaded', 'movie.snatched']

    def notify(self, message = '', data = {}, type = None):
        if self.dontNotify(type): return

        nma = pynma.PyNMA()
        keys = self.conf('api_key').split(',')
        nma.addkey(keys)
        nma.developerkey(self.conf('dev_key'))

        response = nma.push(self.app_name, 'CouchPotato', message, priority = self.priority, batch_mode = len(keys) > 1)

        for key in keys:
            if not response[str(key)]['code'] == u'200':
                log.error('Could not send notification to NotifyMyAndroid (%s). %s' % (key, response[key]['message']))

        return response