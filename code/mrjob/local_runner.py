import sys
from job import MRWordFreqCount

import tempfile
import subprocess

with tempfile.NamedTemporaryFile(suffix=".jpg") as f:
    def get_cam_snapshot(out_file: str, dev: str="/dev/video0"):
        retcode = subprocess.call(
            ["ffmpeg", "-f", "video4linux2", "-i", dev, "-vframes", "1", "-y", "-video_size", "640x480",  f"{out_file}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        if retcode:
            raise Exception(f"Non zero retcode: {retcode}") 
    
    get_cam_snapshot(f.name)

    


if __name__ == '__main__':
    worker = MRWordFreqCount()
    worker.sandbox(open(sys.argv[1], 'rb'))
    
    with worker.make_runner() as runner:
        runner.run()
        for key, value in worker.parse_output(runner.cat_output()):
            print(key, value)