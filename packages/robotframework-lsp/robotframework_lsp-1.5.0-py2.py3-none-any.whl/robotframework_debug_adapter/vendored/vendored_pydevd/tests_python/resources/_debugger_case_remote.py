if __name__ == '__main__':
    import os
    import sys
    port = int(sys.argv[1])
    root_dirname = os.path.dirname(os.path.dirname(__file__))

    if root_dirname not in sys.path:
        sys.path.append(root_dirname)

    del sys.argv

    import pydevd
    print('before pydevd.settrace')
    pydevd.settrace(port=port)
    print('after pydevd.settrace')
    print('TEST SUCEEDED!')
