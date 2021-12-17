FROM maven:3.8-jdk-11 as builder
RUN mkdir -p /tmp/build_jar
COPY . /tmp/build_jar
WORKDIR /tmp/build_jar
RUN mvn -B package --file pom.xml
RUN ls -l /tmp/build_jar

FROM openjdk:8-jdk-alpine
ARG SERVER_PORT=9092
ARG APP_FILE_NAME=example.smallest-0.0.1-SNAPSHOT.war
WORKDIR /opt/app
COPY --from=builder /tmp/build_jar/target /opt/app
COPY application.properties /opt/app/
EXPOSE ${SERVER_PORT}
ENV VAR_APP_FILE_NAME=${APP_FILE_NAME}
ENTRYPOINT java -jar $VAR_APP_FILE_NAME
