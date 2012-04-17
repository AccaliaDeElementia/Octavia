import random

class Chain(object):
    def __len__(self):
        return self.__output_limit

    def __init__(self, items=None,  chain=2, limit=100):
        if not isinstance(chain, int) or chain < 1:
            raise ValueError('chain must be a positive integer')
        if not isinstance(limit, int) or limit < 0:
            raise ValueError('limit must be a non negative integer')
        rand = random.Random()
        self._state = rand.getstate()
        del rand
        self.__chain_length = chain
        self.__output_limit = limit
        self.__table = {}
        if items != None:
            self.insert(items)

    def insert (self, items):
        history = []
        for item in items:
            self.__table.setdefault(tuple(history), []).append(item)
            history.append(item)
            history = history[-self.__chain_length:]

    def has_data(self):
        return len(self.__table) != 0

    def random_state (self, rand):
        return list(rand.choice(self.__table.keys())) 

    def next (self, state, rand):
        items = self.__table.get(tuple(state), [])
        if len(items) == 0:
            return (None, None)
        item = rand.choice(items)
        return (item, state[-(self.__chain_length - 1):]+[item])

    def load(self, file_):
        #TODO
        raise NotImplementedError()

    def save(self, file_):
        #TODO
        raise NotImplementedError()

class FiniteChain (Chain):
    def __iter__(self):
        rand = random.Random()
        rand.setstate(self._state)
        state = self.random_state(rand)
        looped = 0
        while looped < len(self):
            item, state = self.next(state, rand)
            if item == None:
                item, state = self.next(self.random_state(rand), rand)
            looped += 1
            yield item

class InfiniteChain (Chain):
    def __iter__(self):
        rand = random.Random()
        rand.setstate(self._state)
        state = self.random_state(rand)
        while True:
            item, state = self.next(state, rand)
            if item == None:
                item, state = self.next(self.random_state(rand), rand)
            yield item

if __name__ == '__main__':
    fourscore = '''Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.	Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.	But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth.'''

    print 'By the letter, Chains of 2'
    chain =FiniteChain(fourscore, chain=2, limit=100)
    print ''.join(list(chain))
    print ''.join(list(chain))
    print 'By the letter, Chains of 4'
    print ''.join(list(FiniteChain(fourscore, chain=2, limit=100)))    
    print 'By the word, Chains of 2'
    print ' '.join(list(FiniteChain(fourscore.split(), chain=2, limit=1000)))
