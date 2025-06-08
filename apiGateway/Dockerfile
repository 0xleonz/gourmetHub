# apiGateway/Dockerfile
FROM golang:1.19-alpine

WORKDIR /app
COPY main.go .

RUN go mod init gateway
RUN go build -o gateway .

EXPOSE 8080
CMD ["./gateway"]