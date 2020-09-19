#-*- coding:utf-8 -*-
#version v1.0 pkg管理
#本程序用于小说包管理
import sys
import datetime
import os
import time
import base64
import zlib
print("This is NodeEditor v3.0")
outname=""
fpath=""
selfpath=""

if len(sys.argv)==1:
	print("python cnl.py foldername")
	print("文件夹名后不能带斜线")
	sys.exit()
elif len(sys.argv)==2:
	fpath=sys.argv[1]
	outname=f"{datetime.datetime.strftime(datetime.datetime.now(),'%Y_%m_%d_%H_%M_%S')}.txt"
	selfpath=fpath+"/slf/"

print(f"工程路径：{fpath}\n默认输出文件名：{outname}\n自定义节点存储地址：{selfpath}")

nodes=[] #文章所有节点
pkgs={} #导入的所有包
layer=[] #包使用记忆
pos=-2 #光标位置 -1以下是尾部,0是第一段之前
def insertnode(content):
	global pos
	global nodes
	# if pos==-1:
	# 	nodes.insert(0,content)
	# 	pos=0
	if pos==-2:
		nodes.append(content)
	else:
		nodes.insert(pos+1,content)
		pos=pos+1
def readcsv(path,name):
	global pkgs
	print(f"\n{name}包开始导入...")
	s=""
	with open(path,'r',encoding='utf-8-sig') as f:
		s=f.read()
	d=s.split("\n")
	k=[]
	for i in d:
		if i.strip()!="":
			k.append(i)
	csvs={}
	for i in k:
		a=i.replace("\\n","\n")
		makein(a,csvs)
	pkgs[name]=csvs
	print(f"{name}包已经导入完成...\n")


def readpkg(path,name):
	global pkgs
	print(f"\n{name}包开始导入...")
	s=[]
	with open(path,'rb') as f:
		s=f.read()
	s=zlib.decompress(s)
	s=bytearray(s)
	# s=bytearray(s,encoding = "utf-8")
	for i in range(len(s)):
		s[i]=s[i]-1
	s=str(s, encoding = "utf-8")
	s=base64.b64decode(s).decode("utf-8")
	d=s.split("\n")
	k=[]
	for i in d:
		if i.strip()!="":
			k.append(i)
	csvs={}
	for i in k:
		a=i.replace("\\n","\n")
		makein(a,csvs)
	pkgs[name]=csvs
	print(f"{name}包已经导入完成...\n")

#参数为 路径条，字典
def makein(name,dd):
	fx=name.split(",")
	newli=[]
	for i in fx:
		if i=="":
			break
		else:
			newli.append(i)
	x=len(newli)
	k=dd
	z=[]#作为比较用的
	for i in range(x):
		if i<(x-2):
			if newli[i] in k:
				if(type(k[newli[i]])==type(dd)):
					k=k[newli[i]]
					continue
				else:
					k[newli[i]]={}
					k=k[newli[i]]
			else:
				k[newli[i]]={}
				k=k[newli[i]]
		elif i==(x-2):
			if newli[i] in k:
				if(type(k[newli[i]])==type(z)):
					k=k[newli[i]]
					continue
				else:
					k[newli[i]]=[]
					k=k[newli[i]]
			else:
				k[newli[i]]=[]
				k=k[newli[i]]
		else:
			k.append(newli[i])
			k=dd

if __name__ == '__main__':
	while True:
		print("\n=======主菜单========")
		print("\n选择指令：")
		print("-1.不保存退出")
		print("0.保存退出")
		print("1.插入自定义节点(请放在自定义节点地址路径下)")
		print("2.插入工具包节点(必须引用工具包，否则出错)")
		print("3.新建段落")
		print(f"4.删除上一个段落或节点(现光标位置为：{pos})")
		print("5.引用工具包(强制过滤同名包)")
		print("6.预览章节")
		print("7.编辑章节")
		print("8.导出章节")
		print("\n=======菜单尾========")
		select1=input("\n输入指令：")
		select1=select1.strip()
		if select1=="-1":
			print("辛苦了！感谢使用。")
			time.sleep(1)
			print("已退出")
			time.sleep(0.5)
			sys.exit()
		elif select1=="0":
			x=input("请输入每段开头的字符用以排版(默认为空):")
			n=input("请输入章节名(默认为现行时间):")
			if n.strip()!="":
				outname=n+".txt"
			with open(f"{fpath}/{outname}",'w',encoding='utf-8') as f:
				f.write(x)
				for i in nodes:
					k=i.replace("\n",f"\n{x}")
					f.write(k)
			print("已保存")
			time.sleep(0.5)
			print("辛苦了！感谢使用。")
			print("已退出")
			sys.exit()
		elif select1=="1":
			k=os.walk(selfpath)
			a=[]
			for i in k:
				a.append(i)
			a=a[0][2]
			print("\n")
			print("您可以选择的节点有：")
			for i in range(len(a)):
				print(f"{i+1}.{a[i]}")
			z=int(input("请输入你的选择(-1返回上一层)："))
			if(z>len(a) or z<=0):
				print("返回上一层")
				time.sleep(0.5)
				continue
			else:
				with open(f"{selfpath}{a[z-1]}",'r',encoding='utf-8') as f:
					nodes.append(f.read())
				print(f"\n节点{a[z-1].replace('.txt','')}加入完毕\n")
				time.sleep(0.5) #此处为方便用户看见文本
		elif select1=="2":
			print("\n")
			if bool(pkgs)==False:
				print("您需要先导入包")
				time.sleep(0.5)
			else:
				pgs=[]
				# layer=[]
				while True:
					e=pkgs
					# print(layer)
					for i in layer:
						e=e[i]
					if(type(e)==type(pkgs)):
						zd=[]
						for i in e:
							zd.append(i)
						print("\n=========包头==========\n")
						for i in range(len(zd)):
							print(f"{i}.{zd[i]}")
						print("\n=========包尾==========\n")
						ol=input("\n请选择您要使用的包(-1返回上一层):")
						if ol=="":
							ol=-1
						else:
							ol=int(ol)
						if ol<0 or ol>=len(zd):
							print("正在返回上一层")
							if(len(layer)==0):
								time.sleep(0.3)
								break
							else:
								layer.pop()
								time.sleep(0.3)
								continue
						else:
							layer.append(zd[ol])
					else:#不是字典就是列表
						print("\n=========节点头==========\n")
						for i in range(len(e)):
							print(f"{i}.{e[i]}")
						print("\n=========节点尾==========\n")
						ol=input("\n请选择您要使用的节点(-1返回上一层):")
						if ol=="":
							ol=-1
						else:
							ol=int(ol)
						if ol<0 or ol>=len(e):
							print("正在返回上一层")
							# layer.pop()
							if(len(layer)==0):
								time.sleep(0.3)
								break
							else:
								layer.pop()
								time.sleep(0.3)
								continue
						else:
							# nodes.append(e[ol])
							insertnode(e[ol])
							print("已插入节点....")
							time.sleep(0.5)
							break
		elif select1=="3":
			# nodes.append("\n")
			insertnode("\n")
			print("\n已新建段落...\n")
			time.sleep(0.5)
		elif select1=="4":
			if pos==-1 or len(nodes)==0:
				print("当前光标前方无节点")
			elif pos==-2:
				nodes.pop()
			else:
				nodes.pop(pos)
				pos=pos-1
			print("\n已删除上一段落或节点...\n")
			time.sleep(0.5)
		elif select1=="5":
			k=os.walk("pkg")
			a=[]
			for i in k:
				a.append(i)
			e=a[0][2]
			print("\n")
			print("您可以选择的包有：")
			a=[]
			for i in e:
				d=i.replace(".csv","")
				d=d.replace(".pkg","")
				if d in pkgs:
					continue
				else:
					a.append(i) 
			for i in range(len(a)):
				print(f"{i+1}.{a[i]}")
			z=int(input("请输入你的选择(-1返回上一层,0导入所有包)："))
			if(z>len(a) or z<0):
				print("返回上一层")
				continue
			elif z==0:#导入全部
				for i in a:
					if(i.find(".csv")>-1):
						readcsv(f"pkg/{i}",i.replace(".csv",""))
					elif(i.find(".pkg")>-1):
						readpkg(f"pkg/{i}",i.replace(".pkg",""))
					else:
						print("暂不支持此类型文件...")
				print("已经导入全部包")
				time.sleep(0.5) #此处为方便用户看见提示文本
			else:#导入用户选择的包
				if(a[z-1].find(".csv")>-1):
					readcsv(f"pkg/{a[z-1]}",a[z-1].replace(".csv",""))
				elif(a[z-1].find(".pkg")>-1):
					readpkg(f"pkg/{a[z-1]}",a[z-1].replace(".pkg",""))
				else:
					print("暂不支持此类型文件...")
				time.sleep(0.5) #此处为方便用户看见提示文本
		elif select1=="6":
			x=input("请输入每段开头的字符用以排版(默认为空):")
			print("\n=========章节开始==========\n")
			print(x,end="")
			for i in nodes:
				k=i.replace("\n",f"\n\n{x}")
				print(k,end="")
			print("\n\n=========章节结束==========\n")
			time.sleep(0.5)
		elif select1=="7":
			print("\n======章节编辑工具======\n")
			print("-1.返回上一层")
			print(f"1.移动光标至...(现在光标位置为：{pos}。 -1为第一段之前,-2为章节末尾,其它数字即放在相应节点之后。段尾数字为换行符,并非为bug)")
			print("2.删除节点")
			print("3.以段落显示节点(依旧以预览章节的方式输出)")
			print("4.分离显示所有节点(每个节点作为一段显示)")
			print("\n======编辑工具末尾======")
			x7=int(input("\n请选择功能:"))
			if x7==1:
				a=int(input("\n请输入光标位置:"))
				if a<-2 or a>=len(nodes):
					print("输入错误，回上一层")
				elif a==len(nodes)-1:
					pos=-2
					print("光标已放置....")
				else:
					pos=a
					print("光标已放置....")
				time.sleep(0.5)
			elif x7==2:
				a=int(input("\n请输入要删除的节点:"))
				if a<0 or a>=len(nodes):
					print("输入错误，回上一层")
				else:
					nodes.pop(a)
					print("节点已删除....")
				time.sleep(0.5)
			elif x7==3:
				x=input("请输入每段开头的字符用以排版(默认为空):")
				print("\n=========章节开始==========\n")
				print(x,end="")
				for i in range(len(nodes)):
					k=nodes[i].replace("\n",f"\n\n{x}")
					print(f"（{i}#）{k}",end="")
				print("\n\n=========章节结束==========\n")
				time.sleep(0.5)
			elif x7==4:
				print("\n=========章节开始==========\n")
				for i in range(len(nodes)):
					print(f"（{i}#）{nodes[i]}")
				print("\n\n=========章节结束==========\n")
				time.sleep(0.5)
			else:
				print("返回上一层...")
				time.sleep(0.5)
		elif select1=="8":
			x=input("请输入每段开头的字符用以排版(默认为空):")
			n=input("请输入章节名(默认为现行时间):")
			if n.strip()!="":
				outname=n+".txt"
			with open(f"{fpath}/{outname}",'w',encoding='utf-8') as f:
				f.write(x)
				for i in nodes:
					k=i.replace("\n",f"\n{x}")
					f.write(k)
			print("已保存")
			time.sleep(0.5)


