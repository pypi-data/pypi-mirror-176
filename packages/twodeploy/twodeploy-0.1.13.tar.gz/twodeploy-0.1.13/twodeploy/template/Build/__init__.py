nextjs = '''
FROM node:latest
WORKDIR /app
COPY package.json /app
RUN rm -rf deploy/
COPY . /app
RUN export NODE_OPTIONS=--openssl-legacy-provider
RUN yarn install
RUN yarn global add serve
RUN yarn build
'''

reactjs = '''
FROM node:latest
WORKDIR /app
COPY package.json /app
RUN rm -rf deploy/
COPY . /app
RUN export NODE_OPTIONS=--openssl-legacy-provider
RUN yarn install
RUN yarn global add serve
RUN yarn build
'''

def read(arg):
    if(arg == 'nextjs'):
        return nextjs
    if(arg == 'reactjs'):
        return reactjs
    return ''