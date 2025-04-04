from mrjob.job import MRJob
from mrjob.protocol import TextProtocol
import re

WORD_RE = re.compile(r"[\w']+")


class MRWordFreqCount(MRJob):
    OUTPUT_PROTOCOL = TextProtocol
    
    def mapper(self, _, line):
        for word in WORD_RE.findall(line):     
            word = word.lower()   
            self.increment_counter("group_first_letter", "first_letter_" + word[0], 1)
            yield (word, 1)

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, str(sum(counts))
        
        
if __name__ == '__main__':    
    MRWordFreqCount.run()