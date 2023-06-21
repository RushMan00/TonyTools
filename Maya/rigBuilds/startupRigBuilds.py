import sys

def importingPaths():
    print("tony's tool box is working!")
    lstpaths = ['D:\OneDrive\TonyTools\projects',
                ]

    for lst in lstpaths:
        sys.path.append(lst)
        paths = sys.path
        for i in paths:
            print("is imortated" + i)


