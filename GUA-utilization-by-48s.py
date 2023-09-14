# URL of stats 
# https://www.potaroo.net/bgp/stats/nro/delegated-nro-extended

# Local file location
# /Users/tom/Dropbox/VS Code/dev/tmp/delegated-nro-extended.txt
# ipv6 = open('/Users/tom/Dropbox/VS Code/dev/tmp/delegated-nro-extended.txt')

import re
import shutil
import tempfile
import urllib.request
import os

# with urllib.request.urlopen('https://www.potaroo.net/bgp/stats/nro/delegated-nro-extended') as response:
#     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#         shutil.copyfileobj(response, tmp_file)

# for var1 in range(19, 49):
#         ipv6 = open(tmp_file.name)
#         print(len(re.findall(rf"ipv6.*::\|{var1}.*assigned", ipv6.read())))

# os.remove(tmp_file.name)

from io import StringIO
import sys
from jinja2 import Template
import numpy
import ast

tmp = sys.stdout
my_result = StringIO()
sys.stdout = my_result

for var1 in range(19, 49):
        ipv6 = open('/Users/tom/Dropbox/VS Code/dev/tmp/delegated-nro-extended.txt')
        print(len(re.findall(rf"ipv6.*::\|{var1}.*assigned", ipv6.read())))

sys.stdout = tmp

# print(my_result.getvalue())
allocated_48s = (str.split(my_result.getvalue()))
allocated_48s = [ast.literal_eval(i) for i in allocated_48s]

cidr_length = []
for i in range(19, 49):
    i = cidr_length.append(str(f"/{i}"))

available_48s = [536870912 ,268435456 ,134217728 ,67108864 ,33554432 ,16777216 \
                ,8388608 ,4194304 ,2097152 ,1048576 ,524288 ,262144 ,131072 ,65536 \
                ,32768 ,16384 ,8192 ,4096 ,2048 ,1024 ,512 ,256 ,128 ,64 ,32 ,16 ,8 ,4 ,2 ,1]

total_48s = numpy.multiply(allocated_48s, available_48s)

cidr_allocated_totals = zip(cidr_length, allocated_48s, total_48s)

# Create one external form_template html page and read it
File = open('index-template.html', 'r')
content = File.read()
File.close()

# Render the template and pass the variables
template = Template(content)
rendered_form = template.render(cidr_allocated_totals=cidr_allocated_totals)

# save the txt file in the form.html
output = open('index.html', 'w')
output.write(rendered_form)
output.close()