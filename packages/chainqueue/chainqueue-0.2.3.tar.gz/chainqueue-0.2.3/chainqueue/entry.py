# standard imports
import logging

# external imports
from hexathon import (
        add_0x,
        strip_0x,
        uniform,
        )

# local imports
from chainqueue.cache import CacheTx

logg = logging.getLogger(__name__)


def normalize_hex(k):
    k = strip_0x(k)
    return uniform(k)


class QueueEntry:

    def __init__(self, store, tx_hash=None, cache_adapter=CacheTx):
        self.store = store
        #self.tx_hash = normalize_hex(tx_hash)
        self.tx_hash = tx_hash
        self.signed_tx = None
        self.seq = None
        self.k = None
        self.synced = False
        self.cache_adapter = cache_adapter


    def serialize(self):
        return self.signed_tx


    def create(self, signed_tx):
        signed_tx = normalize_hex(signed_tx)
        (s, tx_hash) = self.store.put(signed_tx, cache_adapter=self.cache_adapter)
        self.k = s
        self.synced = True
        return tx_hash


    def local_state(self):
        state = self.store.state(self.k)
        state_str = self.store.name(state)
        return (state, state_str,)


    def load(self):
        (self.k, self.signed_tx) = self.store.get(self.tx_hash)
        self.synced = True


    def __match_state(self, state):
        return bool(self.store.state(self.k) & state)

    
    def waitforfunds(self):
        if self.__match_state(self.store.INSUFFICIENT_FUNDS):
            return
        self.store.move(self.k, self.store.INSUFFICIENT_FUNDS)


    def fubar(self):
        if self.__match_state(self.store.UNKNOWN_ERROR):
            return
        self.store.set(self.k, self.store.UNKNOWN_ERROR)


    def reject(self):
        if self.__match_state(self.store.NODE_ERROR):
            return
        self.store.set(self.k, self.store.NODE_ERROR)


    def override(self, manual=False):
        if manual:
            self.store.set(self.k, self.store.OBSOLETE | self.store.MANUAL)
        else:
            self.store.set(self.k, self.store.OBSOLETE)


    def manual(self):
        self.store.set(self.k, self.store.MANUAL)


    def retry(self):
        if self.__match_state(self.store.QUEUED):
            return
        self.store.change(self.k, self.store.QUEUED, self.store.INSUFFICIENT_FUNDS)


    def readysend(self):
        if self.__match_state(self.store.QUEUED):
            return
        self.store.change(self.k, self.store.QUEUED, self.store.INSUFFICIENT_FUNDS)

    
    def sent(self):
        if self.__match_state(self.store.IN_NETWORK):
            return
        self.store.change(self.k, self.store.IN_NETWORK, self.store.RESERVED | self.store.DEFERRED | self.store.QUEUED | self.store.LOCAL_ERROR | self.store.NODE_ERROR)


    def sendfail(self):
        if self.__match_state(self.store.NODE_ERROR):
            return
        self.store.change(self.k, self.store.LOCAL_ERROR | self.store.DEFERRED, self.store.RESERVED | self.store.QUEUED | self.store.INSUFFICIENT_FUNDS)


    def reserve(self):
        if self.__match_state(self.store.RESERVED):
            return
        self.store.change(self.k, self.store.RESERVED, self.store.QUEUED) 


    def fail(self, block, tx):
        if self.__match_state(self.store.NETWORK_ERROR):
            return
        v = self.store.state(self.k)
        self.store.change(self.k, v | self.store.NETWORK_ERROR, self.store.QUEUED)
        if self.store.cache:
            self.store.cache.set_block(self.tx_hash, block, tx)


    def cancel(self, confirmed=False):
        if confirmed:
            self.store.change(self.k, self.store.OBSOLETE | self.store.FINAL, self.store.RESERVED | self.store.QUEUED)
        else:
            self.store.change(self.k, self.store.OBSOLETE, self.store.RESERVED | self.store.QUEUED)


    def succeed(self, block, tx):
        self.store.set(self.k, self.store.FINAL)
        if self.store.cache:
            self.store.cache.set_block(self.tx_hash, block, tx)


    def test(self, state):
        return self.__match_state(state)


    def __str__(self):
        v = self.store.get(self.tx_hash)
        n = self.store.state(v[0])
        s = self.store.name(n)
        return '{}: {} ({})'.format(self.k, s, n)
