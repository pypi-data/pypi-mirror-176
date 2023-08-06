nextjs = '''
serve -s build -p $1
'''

reactjs = '''
serve -s build -p $1
'''

def read(arg):
    if(arg == 'nextjs'):
        return nextjs
    if(arg == 'reactjs'):
        return reactjs
    return ''