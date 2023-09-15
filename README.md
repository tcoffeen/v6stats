# v6stats
GUA-utilization-by-48s.py grabs all the IPv6 RIR data from https://www.potaroo.net/bgp/stats/nro/delegated-nro-extended, extracts all RIR IPv6 CIDR allocations from /19 through /48 to determine percentage utilization of the GUA (2000::/3), writes the results using index-template.html, and uploads the resulting index.html to an S3 bucket website (https://stats.ipv6enabled.net).
