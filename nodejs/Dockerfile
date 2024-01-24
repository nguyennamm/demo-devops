FROM node:16
# Create app directory
WORKDIR /usr/src/app

# ARG MYSQL_USER
# ENV MYSQL_USER=${MYSQL_USER}

# ARG MYSQL_PASSWORD
# ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}

# Install app dependencies
# Copy both package.json AND package-lock.json to the working directory
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

EXPOSE 3000
CMD npm start
