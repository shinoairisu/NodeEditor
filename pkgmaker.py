#-*- coding:utf-8 -*-
#version v1.0 小说包制作
import sys
import time
import base64
import zlib
print("This is pkgmaker v3.0")
a=sys.argv[0]
codes=""
outname=""
if len(sys.argv)==1:
	print("python pkgmaker.py name.csv")
	print("csv必须是BOM-utf-8")
	sys.exit()
elif len(sys.argv)==2:
	s=""
	with open(sys.argv[1],'r',encoding='utf-8-sig') as f:
		codes=f.read()
	outname=sys.argv[1].replace(".csv",".pkg")
	print("读取完毕...")
codes=codes.encode("utf-8")
ncodes=base64.b64encode(codes)
ncodes=bytearray(ncodes)
print("开始转换...")
for i in range(len(ncodes)):
	ncodes[i]=ncodes[i]+1
# ncodes=str(ncodes, encoding = "utf-8")
print("开始链接组装...")
ncodes=zlib.compress(ncodes)
with open(outname,'wb') as f:
		f.write(ncodes)
print(f"写出到{outname}成功!")


