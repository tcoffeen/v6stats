import re
import shutil
import tempfile
import urllib.request
import os
from io import StringIO
import sys
from jinja2 import Template
import numpy
import ast
import boto3
from urllib import parse
from datetime import datetime, timezone

# Grab raw allocation data from Geoff Huston's site and write it to a temp file
with urllib.request.urlopen('https://www.potaroo.net/bgp/stats/nro/delegated-nro-extended') as response:
     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

# redirect stdout (to silence print function in next clause)
tmp = sys.stdout
my_result = StringIO()
sys.stdout = my_result

# regex to grab assigned v6 CIDRs and print count
for var1 in range(19, 49):
        ipv6 = open(tmp_file.name)
        print(len(re.findall(rf"ipv6.*::\|{var1}.*assigned", ipv6.read())))

# re-redirect stdout
sys.stdout = tmp

# format assigned v6 CIDR count and remove quotes for numpy multiply
# (There's probably a trivial way to do this in one line but I suck)
allocated_cidrs = (str.split(my_result.getvalue()))
allocated_cidrs = [ast.literal_eval(i) for i in allocated_cidrs]

# generate and format a list of cidr lengths between /19 and /48 
cidr_length = []
for i in range(19, 49):
    i = cidr_length.append(str(f"/{i}"))

# define list of total /48s available for listed CIDR lengths
available_48s = [536870912 ,268435456 ,134217728 ,67108864 ,33554432 ,16777216 \
                ,8388608 ,4194304 ,2097152 ,1048576 ,524288 ,262144 ,131072 ,65536 \
                ,32768 ,16384 ,8192 ,4096 ,2048 ,1024 ,512 ,256 ,128 ,64 ,32 ,16 ,8 ,4 ,2 ,1]

# multiply allocated v6 CIDRs by number of /48s in that CIDR, add up all of the allocated /48s 
# and calculate percentage of allocated /48s in 2000::/3
total_48s = numpy.multiply(allocated_cidrs, available_48s)
total_48s_sum = numpy.sum(total_48s)
percent = (total_48s_sum) / 35184372088832 * 100
perc_round = round(percent, 2)

# Define time and date stamp
dt_string = datetime.now(timezone.utc)
timedatestamp = dt_string.strftime("%m/%d/%Y %H:%M:%S")

# create single list that includes CIDR lengths from /19 to /48, 
# the allocated CIDRs, and the total /48s consumed for all CIDR
template_data = zip(cidr_length, allocated_cidrs, total_48s)

# Create one external form_template html page and read it
File = open('/Users/tom/Dropbox/VS Code/dev/v6stats/index-template.html', 'r')
content = File.read()
File.close()

# Render the template and pass the variables
template = Template(content)
rendered_form = template.render(template_data=template_data, total_48s_sum=total_48s_sum, perc_round=perc_round, timedatestamp=timedatestamp)

# save the txt file in the form.html
output = open('/Users/tom/Dropbox/VS Code/dev/v6stats/index.html', 'w')
output.write(rendered_form)
output.close()

# remove tmp file
os.remove(tmp_file.name)

# Upload new index.html to S3 bucket website
s3 = boto3.resource('s3')
tags = {"public": "yes"}
s3 = boto3.client('s3')
s3.upload_file('index.html', 'stats.ipv6enabled.net', 'index.html', ExtraArgs={'Tagging': parse.urlencode(tags), 'ContentType': "text/html"})