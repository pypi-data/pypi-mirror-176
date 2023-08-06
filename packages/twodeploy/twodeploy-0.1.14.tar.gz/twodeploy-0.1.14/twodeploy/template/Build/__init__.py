from ..utils import nextjs, reactjs

def read(arg):
    if(arg == 'nextjs'):
        return nextjs
    if(arg == 'reactjs'):
        return reactjs
    return ''