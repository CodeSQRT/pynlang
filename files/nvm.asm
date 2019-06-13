@entry start

start:

	mov ax,"старт",str

	mov argc,1,int
	mov arg1,"ку",str

	call print
	std out,ax,var
.end

get:
	mov ax,"гет",str
	std out,ax,var
.end

print:
	mov eax,"принт",str
	mov ebx,123,int
	call get
	mov ret,null,var
	std out,eax,var
.end