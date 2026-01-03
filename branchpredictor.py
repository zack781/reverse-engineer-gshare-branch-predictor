def make_predictor(bhr_size, sat_counter_bits, pc_bits_used):
    class SaturatingCounter(object):
        def __init__(self, bits, init):
            self.max = (2 ** bits) - 1
            self.value = init
            pass

        def taken(self):
            if self.value + 1 <= self.max:
                self.value += 1
            pass

        def nottaken(self):
            if self.value - 1 >= 0:
                self.value -= 1
            pass

        def istaken(self):
            # print ((self.max+1)/2)
            return self.value >= ((self.max+1)/2)

    class ShiftRegister(object):
        def __init__(self,size):
            self.size = size
            self.values = []
            for i in range( size ):
                self.values.append( False )
            pass

        def push(self,val):
            assert isinstance( val, bool )
            self.values.append( val )
            if ( len(self.values) > self.size ):
                self.values.pop( 0 )

        def tobits(self):
            t = 0
            # print self.values
            for i in range( len(self.values) ):
                t = t << 1
                if self.values[i]:
                    t = t | 1
                else:
                    t = t | 0
            return t

    class MysteryBranchPredictor(object):
        def __init__(self):
            self.bht = {}
            self.bhr = ShiftRegister( bhr_size )
            self.pcmask = (2 ** pc_bits_used) - 1
            self.reset()
            pass

        def reset(self):
            # reset bht
            sc_init_val = ((2 ** sat_counter_bits )-1) / 2
            bht_entries = 2 ** ( pc_bits_used + bhr_size )
            # print("bht_entries = ", bht_entries)
            for i in range( bht_entries ):
                self.bht[i] = SaturatingCounter( sat_counter_bits, sc_init_val )
                pass
            # reset gh
            for i in range( bhr_size ):
                self.bhr.push( False )

        def _compute_index(self,pc):
            pcbits = pc & self.pcmask
            ghbits = self.bhr.tobits()
            # print (ghbits << pc_bits_used) | pcbits
            return (ghbits << pc_bits_used) | pcbits

        def predict(self, pc):
            index = self._compute_index( pc )
            return self.bht[ index ].istaken()

        def actual(self, pc, taken):
            index = self._compute_index( pc )
            if taken:
                self.bht[ index ].taken()
            else:
                self.bht[ index ].nottaken()
                pass

            self.bhr.push( taken )

    return MysteryBranchPredictor()

mystery_predictors = [
    ('2bhr, 2sc, 16bht',   make_predictor(2, 2, 2)),
    ('3bhr, 1sc, 64bht',   make_predictor(3, 1, 3)),
    ('8bhr, 4sc, 2048bht', make_predictor(8, 4, 3)),
]
