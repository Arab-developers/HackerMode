import os,shutil,sys

class Del:

	def __init__(self):
		self.base = os.path.join(os.environ['HOME'],".trash")
		self.usage = f'''
\033[1;32m
trash path 	:	{self.base}
options:
	-h 	:	select hidden files/dirs
	-c	:	clear the cache of the trash file
	--help	:	show this menu
Examples:
	del file.txt data.py main.css
	del folder1
	del *
	del -h *
	del -h -c
	del -c
\033[0m			'''
		#self.base = os.path.join(os.environ['HOME'],".trash")
		if os.path.exists(self.base):pass
		else:os.mkdir(self.base)
		args= ['--help','-c','-h']
		self.arg1 = sys.argv[1:]
		for j in args:
			if j in self.arg1:self.arg1.remove(j)
		self.arg2 = sys.argv[1:]
		self.hide=0
	def clear_cache(self):
		all = os.listdir(self.base) if self.hide else [x for x in os.listdir(self.base) if not x.startswith('.')]
		for x in all:
			full = os.path.join(self.base,x)
			if os.path.isfile(full):os.remove(full)
			else:shutil.rmtree(full)

	def delete(self,p):
		try:
			if os.path.exists(p):shutil.move(p,self.base)
		except shutil.Error:
			to = os.path.join(self.base,p)
			print(f'File Existed in {to}')
			i=input('Do you wnat to override the file [y/n]')
			if i.lower() in 'yesy':
				if os.path.isfile(p):os.remove(to)
				else:shutil.rmtree(to)
				return self.delete(p)
		except Exception as e:
			print(e)

	def main(self):
		if len(self.arg2) < 1:print(self.usage)
		if '-h' in self.arg2:self.hide=1
		if '-c' in self.arg2:self.clear_cache()
		for a in self.arg1:
			if a=='*':
				h=os.listdir() if self.hide else [ x for x in self.arg1 if not x.startswith('.')]
				for b in h:self.delete(b)
			if a.startswith('.') or self.hide:
				self.delete(a)
			else:
				args = [ x for x in self.arg1 if not x.startswith('.')]
				for b in args:
					self.delete(b)

if __name__ == '__main__':
	Del().main()

