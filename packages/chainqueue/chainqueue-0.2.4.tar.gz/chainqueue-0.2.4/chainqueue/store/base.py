# standard imports
import re
import datetime
import logging
import time

# local imports
from chainqueue.cache import CacheTx
from chainqueue.entry import QueueEntry
from chainqueue.error import NotLocalTxError
from chainqueue.enum import (
        StatusBits,
        all_errors,
        )

logg = logging.getLogger(__name__)


def to_key(t, n, k):
    return '{}_{}_{}'.format(t, n, k)


def from_key(k):
    (ts_str, seq_str, tx_hash) = k.split('_')
    return (float(ts_str), int(seq_str), tx_hash, )

all_local_errors = all_errors() - StatusBits.NETWORK_ERROR

re_u = r'^[^_][_A-Z]+$'
class Store:

    def __init__(self, chain_spec, state_store, index_store, counter, cache=None, sync=True):
        self.chain_spec = chain_spec
        self.cache = cache
        self.state_store = state_store
        self.index_store = index_store
        self.counter = counter
        for s in dir(self.state_store):
            if not re.match(re_u, s):
                continue
            v = self.state_store.from_name(s)
            setattr(self, s, v)
        for v in [
                'state',
                'change',
                'set',
                'unset',
                'name',
                'modified',
                'purge',
                ]:
            setattr(self, v, getattr(self.state_store, v))

        if not sync:
            return

        sync_err = None
        try:
            self.state_store.sync()
        except Exception as e:
            sync_err = e

        if sync_err != None:
            raise FileNotFoundError(sync_err)


    def put(self, v, cache_adapter=CacheTx):
        tx = cache_adapter(self.chain_spec)
        tx.deserialize(v)
        k = tx.hash
        n = self.counter.next()
        t = datetime.datetime.now().timestamp()
        s = to_key(t, n, k)
        self.index_store.put(k, s)
        self.state_store.put(s, v)
        if self.cache != None:
            self.cache.put(self.chain_spec, tx) 
        return (s, k,)


    def get(self, k):
        v = None
        s = self.index_store.get(k)
        err = None
        try:
            v = self.state_store.get(s)
        except FileNotFoundError as e:
            err = e
        if v == None:
            raise NotLocalTxError('could not find tx {}: {}'.format(k, err))
        return (s, v,)


    def by_state(self, state=0, not_state=0, include_pending=False, limit=4096, strict=False, threshold=None):
        hashes = []
        i = 0
  
        refs_state = []
        if state > 0:
            if self.state_store.is_pure(state):
                refs_state = self.state_store.list(state)
            elif strict:
                refs_state = self.state_store.list(state)
            else:
                for v in self.state_store.elements(state, numeric=True):
                    refs_state += self.state_store.list(v)
                refs_state = list(set(refs_state))
        if include_pending:
            refs_state += self.state_store.list(0)

        refs_state.sort()

        for ref in refs_state:
            v = from_key(ref)
            hsh = v[2]

            item_state = self.state_store.state(ref)

            if strict:
                if item_state & state != item_state:
                    continue

            if item_state & not_state > 0:
                continue

            item_state_str = self.state_store.name(item_state)
            logg.info('state {} {} ({})'.format(ref, item_state_str, item_state))

            if threshold != None:
                v = self.state_store.modified(ref)
                if v > threshold:
                    continue

            hashes.append(hsh)

            i += 1
            if limit > 0 and i == limit:
                break

        #hashes.sort()
        return hashes


    def upcoming(self, limit=4096):
        return self.by_state(state=self.QUEUED, limit=limit)


    def deferred(self, limit=4096, threshold=None):
        return self.by_state(state=self.DEFERRED, limit=limit, threshold=threshold)


    def failed(self, limit=4096):
        #return self.by_state(state=all_local_errors, limit=limit)
        r = []
        r += self.by_state(state=self.LOCAL_ERROR, limit=limit)
        r += self.by_state(state=self.NODE_ERROR, limit=limit)
        r.sort()
        if len(r) > limit:
            r = r[:limit]
        return r


    def pending(self, limit=4096):
        return self.by_state(include_pending=True, limit=limit, strict=True)


    def reserve(self, k):
        entry = QueueEntry(self, k)
        entry.load()
        entry.reserve()


    def enqueue(self, k):
        entry = QueueEntry(self, k)
        entry.load()
        try:
            entry.retry()
        except StateTransitionInvalid:
            entry.readysend()


    def fail(self, k):
        entry = QueueEntry(self, k)
        entry.load()
        logg.debug('fail {}'.format(k))
        entry.sendfail()


    def final(self, k, block, tx, error=False):
        entry = QueueEntry(self, k)
        entry.load()
        if error:
            entry.fail(block, tx)
        else:
            entry.succeed(block, tx)


    def send_start(self, k):
        entry = QueueEntry(self, k)
        entry.load()
        entry.reserve()
        return entry


    def send_end(self, k):
        entry = QueueEntry(self, k)
        entry.load()
        entry.sent()


    def is_reserved(self, k):
        entry = QueueEntry(self, k)
        entry.load()
        return entry.test(self.RESERVED)


    def sync(self):
        self.state_store.sync()
