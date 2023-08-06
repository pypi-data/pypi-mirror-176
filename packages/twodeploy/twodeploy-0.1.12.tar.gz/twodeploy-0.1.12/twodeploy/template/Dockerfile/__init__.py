nextjs = '''
FROM node:latest
WORKDIR /app
COPY package.json /app
RUN rm -rf deploy/
COPY . /app
RUN export NODE_OPTIONS=--openssl-legacy-provider
RUN yarn install
RUN yarn build
RUN yarn global add serve
CMD ["bash","ponServer.sh", "PORT_HERE"]
'''

reactjs = '''
FROM node:latest
WORKDIR /app
COPY package.json /app
RUN rm -rf deploy/
COPY . /app
RUN export NODE_OPTIONS=--openssl-legacy-provider
RUN yarn install
RUN yarn build
RUN yarn global add serve
CMD ["bash","ponServer.sh", "PORT_HERE"]
'''

def read(arg):
    if(arg == 'nextjs'):
        return nextjs
    if(arg == 'reactjs'):
        return reactjs
    return ''