nextjs = '''
FROM node:latest
WORKDIR /app
COPY package.json /app
RUN rm -rf deploy/
COPY . /app
RUN yarn install
RUN yarn build
COPY ./ponServer.sh /
RUN chmod +x /ponServer.sh
ENTRYPOINT ["/ponServer.sh"]
'''

reactjs = '''
FROM node:latest
WORKDIR /app
COPY package.json /app
RUN rm -rf deploy/
COPY . /app
RUN yarn install
RUN yarn global add serve
RUN yarn build
COPY ./ponServer.sh /
RUN chmod +x /ponServer.sh
ENTRYPOINT ["/ponServer.sh"]
'''

