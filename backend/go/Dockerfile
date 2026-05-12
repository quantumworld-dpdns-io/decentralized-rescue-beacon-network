FROM golang:1.23-alpine AS builder

WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o /app/beacon-go ./cmd/server

FROM alpine:3.20
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -u 10014
WORKDIR /app
COPY --from=builder /app/beacon-go /app/beacon-go
RUN chown appuser:appgroup /app
USER 10014
EXPOSE 8080
CMD ["/app/beacon-go"]
