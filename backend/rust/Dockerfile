FROM rust:1.81-slim-bookworm AS builder

WORKDIR /build
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release 2>/dev/null || true
RUN rm -rf src

COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin -u 10014 appuser
WORKDIR /app
COPY --from=builder /build/target/release/beacon-rust /app/beacon-rust
RUN chown appuser:appgroup /app
USER 10014
EXPOSE 9090
CMD ["/app/beacon-rust"]
