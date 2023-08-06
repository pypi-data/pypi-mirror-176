nextjs = '''#!/bin/bash
yarn prodPort $FOO
# echo $FOO
'''

reactjs = '''#!/bin/bash
serve -s build -p $FOO
# echo $FOO
'''

def read(arg):
    if(arg == 'nextjs'):
        return nextjs
    if(arg == 'reactjs'):
        return reactjs
    return ''