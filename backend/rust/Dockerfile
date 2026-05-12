FROM rust:1.81-slim-bookworm AS builder
WORKDIR /build
COPY backend/rust/ .
RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /build/target/release/beacon-rust /app/beacon-rust
EXPOSE 9090
CMD ["/app/beacon-rust"]
