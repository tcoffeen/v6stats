# v6stats
GUA-utilization-by-48s.py grabs all the IPv6 RIR data from https://www.potaroo.net/bgp/stats/nro/delegated-nro-extended, extracts all RIR IPv6 CIDR allocations from /16 through /48 to determine percentage utilization of the GUA (2000::/3), writes the results using index-template.html, and uploads the resulting index.html to an S3 bucket website (https://stats.ipv6enabled.net).

When running as a container, pass AWS CLI credentials at runtime; e.g., docker run -e AWS_ACCESS_KEY_ID="key ID" -e AWS_SECRET_ACCESS_KEY="secret key id" v6stats:0.0.1
