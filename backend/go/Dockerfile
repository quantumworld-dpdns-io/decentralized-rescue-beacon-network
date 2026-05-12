FROM golang:1.23-alpine AS builder

WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o /app/beacon-go ./cmd/server

FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/beacon-go /app/beacon-go
EXPOSE 8080
CMD ["/app/beacon-go"]
