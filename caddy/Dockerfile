# Only used in production
FROM caddy:2-builder AS builder

RUN xcaddy build

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
