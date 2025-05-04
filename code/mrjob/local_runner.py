import sys
from job import MRWordFreqCount


if __name__ == '__main__':
    worker = MRWordFreqCount()
    worker.sandbox(open(sys.argv[1], 'rb'))
    
    with worker.make_runner() as runner:
        runner.run()
        for key, value in worker.parse_output(runner.cat_output()):
            print(key, value)