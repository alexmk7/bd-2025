import time 

from kazoo.client import KazooClient


def election_func():
    print("Election won")
    print("Doing something")
    
    time.sleep(50)


def main():
    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()    

    election = zk.Election("/node")    
    print("Waiting for election")
    
    election.run(election_func)
    

if __name__ == "__main__":
    main()