#coding:UTF-8
import sys
def sys_module():
	print("程序包含模块:%s" % sys.modules)
	print("程序加载路径:%s" % sys.path)
	print("程序运行平台:%s" % sys.platform)
	print("程序默认编码:%s" % sys.getdefaultencoding())
	