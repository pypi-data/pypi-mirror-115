import sys
import Digraph

def read_DOT(filepath):
    with open(filepath, 'r') as f:
        dot = f.read()

    print(dot)


#read_DOT('../GUI/MOM.dot')
if __name__ == "__main__":
    Digraph.dot2choices(sys.argv[1])
