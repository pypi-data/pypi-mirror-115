#coding:UTF-8
import sys
def sys_argv():
	if len(sys.argv) == 1:
		print("程序没有输入参数！！！")
		sys.exit(0)
	else:
		print("程序输入参数",end="")
		for item in sys.argv:
			print(item,end="、")