from mrjob.job import MRJob
from mrjob.protocol import TextProtocol
import re

WORD_RE = re.compile(r"[\w']+")


class MRWordFreqCount(MRJob):
    
    def mapper(self, _, line):
        words = WORD_RE.findall(line)
        for idx1 in range(len(words)):
            for idx2 in range(max(idx1-2, 0), min(idx1+2, len(words))):
                word1 = words[idx1].lower()
                word2 = words[idx2].lower()
                if word1 > word2:
                    word2, word1 = word1, word2 
                yield (word1, word2), 1

    def combiner(self, word, counts): 
        yield word, sum(counts)

    def reducer(self, word, counts):  
        yield word, sum(counts)     
        
        
if __name__ == '__main__':    
    MRWordFreqCount.run()