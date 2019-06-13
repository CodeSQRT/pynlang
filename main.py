import sys
from nlang import NLang
import os
def main():
	os.system("cls")
	if "--console" in sys.argv:
		if "--nvm" in sys.argv:
			import nvm
			asm = nvm.Nvm(filename="files/nvm.asm")
			asm.start()
			# print(asm.execute("ax"))
			# print(asm.stack)
			# vm.execute("mov ax,5,int")
			# vm.execute("mov az,2,int")
			# vm.execute("div ax,2,int")
			# print("ax=" + str(vm.execute("ax")))
			return
			# while True:
			# 	text = input(">>>")
			# 	if text == "exit":
			# 		exit()
			# 	elif text == "dump":
			# 		print(vm.variables)
			# 	else:
			# 		print(vm.execute(text))
	
	nlang = NLang("files/test.py")
	nlang.run()
main()