# OrderedBunch.py
#
# Created:  Aug 2015, T. Lukacyzk
# Modified: Feb 2016, T. MacDonald

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

from Bunch import Bunch
from OrderedDict import OrderedDict
from Property import Property
    
# ----------------------------------------------------------------------
#   Ordered Bunch
# ----------------------------------------------------------------------

class OrderedBunch(OrderedDict):
    """ An ordered dictionary that provides attribute-style access.
    """
    
    _root = Property('_root')
    _map  = Property('_map')

    def __delattr__(self, key):
        """od.__delitem__(y) <==> del od[y]"""
        # Deleting an existing item uses self._map to find the link which is
        # then removed by updating the links in the predecessor and successor nodes.
        OrderedDict.__delattr__(self,key)
        link_prev, link_next, key = self._map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev
        
    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''
        if isinstance(other, (OrderedBunch,OrderedDict)):
            return len(self)==len(other) and self.items() == other.items()
        return dict.__eq__(self, other)
        
    def __len__(self):
        return self.__dict__.__len__()   

    def __iter__(self):
        """od.__iter__() <==> iter(od)"""
        root = self._root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]
    
    def __new__(klass,*args,**kwarg):

        self = OrderedDict.__new__(klass)
        
        if hasattr(self,'_root'):
            self._root
        else:
            root = [] # sentinel node
            root[:] = [root, root, None]
            dict.__setitem__(self,'_root',root)
            dict.__setitem__(self,'_map' ,{})
        
        return self

    def __reduce__(self):
        """Return state information for pickling"""
        items = [( k, OrderedBunch.__getitem__(self,k) ) for k in OrderedBunch.iterkeys(self)]
        inst_dict = vars(self).copy()
        for k in vars(OrderedBunch()):
            inst_dict.pop(k, None)
        return (_reconstructor, (self.__class__,items,), inst_dict)
    
    
    # prettier printing
    def __repr__(self):
        """ Invertible* string-form of a Dict.
        """
        keys = self.keys()
        args = ', '.join(['%s=%r' % (key, self[key]) for key in keys if not key.startswith('_')])
        return '%s(%s)' % (self.__class__.__name__, args)
    

    def __setattr__(self, key, value):
        """od.__setitem__(i, y) <==> od[i]=y"""
        # Setting a new item creates a new link which goes at the end of the linked
        # list, and the inherited dictionary is updated with the new key/value pair.
        if not hasattr(self,key) and not hasattr(self.__class__,key):
        #if not self.has_key(key) and not hasattr(self.__class__,key):
            root = dict.__getitem__(self,'_root')
            last = root[0]
            map  = dict.__getitem__(self,'_map')
            last[1] = root[0] = map[key] = [last, root, key]
        OrderedDict.__setattr__(self,key, value)


    def __setitem__(self,k,v):
        self.__setattr__(k,v)

    def clear(self):
        """od.clear() -> None.  Remove all items from od."""
        try:
            for node in self._map.itervalues():
                del node[:]
            root = self._root
            root[:] = [root, root, None]
            self._map.clear()
        except AttributeError:
            pass
        self.__dict__.clear()
        
    def get(self,k,d=None):
        return self.__dict__.get(k,d)
        
    def has_key(self,k):
        return self.__dict__.has_key(k)

    def to_dict(self):
        r = {}
        for k,v in self.items():
            if isinstance(v,OrderedDict):
                v = v.to_dict()
            r[k] = v
        return r
        
    def update(self,other):
        """ Dict.update(other)
            updates the dictionary in place, recursing into additional
            dictionaries inside of other
            
            Assumptions:
              skips keys that start with '_'
        """
        if not isinstance(other,dict):
            raise TypeError , 'input is not a dictionary type'
        for k,v in other.iteritems():
            # recurse only if self's value is a Dict()
            if k.startswith('_'):
                continue
        
            try:
                self[k].update(v)
            except:
                self[k] = v
        return 


    # allow override of iterators
    __iter = __iter__
    __getitem__ = OrderedDict.__getattribute__
    
    def keys(self):
        """OrderedDict.keys() -> list of keys in the dictionary"""
        return list(self.__iter())
    
    def values(self):
        """OrderedDict.values() -> list of values in the dictionary"""
        return [self[key] for key in self.__iter()]
    
    def items(self):
        """OrderedDict.items() -> list of (key, value) pairs in the dictionary"""
        return [(key, self[key]) for key in self.__iter()]
    
    def iterkeys(self):
        """OrderedDict.iterkeys() -> an iterator over the keys in the dictionary"""
        return self.__iter()
    
    def itervalues(self):
        """OrderedDict.itervalues -> an iterator over the values in the dictionary"""
        for k in self.__iter():
            yield self[k]
    
    def iteritems(self):
        """od.iteritems -> an iterator over the (key, value) items in the dictionary"""
        for k in self.__iter():
            yield (k, self[k])    

    
# for rebuilding dictionaries with attributes
def _reconstructor(klass,items):
    self = OrderedBunch.__new__(klass)
    OrderedBunch.__init__(self,items)
    return self
        
        

# ----------------------------------------------------------------------
#   Module Tests
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    o = OrderedBunch()
    print 'should be zero:' , len(o)
    
    o['x'] = 'hello'
    o.y = 1
    o['z'] = [3,4,5]
    o.t = OrderedBunch()
    o.t['h'] = 20
    o.t.i = (1,2,3)
    
    print o

    import pickle

    d = pickle.dumps(o)
    p = pickle.loads(d)
    
    print ''
    print p    

    o.t['h'] = 'changed'
    p.update(o)
    
    print ''
    print p
    
    class TestClass(OrderedBunch):
        a = Property('a')
        def __init__(self):
            self.a = 'hidden!'
            self.b = 'hello!'
    
    c = TestClass()
    print c
    
    