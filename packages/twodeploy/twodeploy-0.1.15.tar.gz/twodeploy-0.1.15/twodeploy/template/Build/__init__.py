from ..utils import nextjs, reactjs, nodejs

def read(arg):
    if(arg == 'nextjs'):
        return nextjs
    if(arg == 'reactjs'):
        return reactjs
    if(arg == 'nodejs'):
        return nodejs                
    return ''