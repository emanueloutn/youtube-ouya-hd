import struct,zipfile,pathlib,sys

def strings(b):
 p=8
 while p<len(b):
  t,h,n=struct.unpack_from('<HHI',b,p)
  if t==1:break
  p+=n
 count,styles,flags,start,_=struct.unpack_from('<5I',b,p+8)
 def l8(o):
  v=b[o];return (((v&127)<<8)|b[o+1],o+2) if v&128 else (v,o+1)
 def l16(o):
  v=struct.unpack_from('<H',b,o)[0];return (((v&32767)<<16)|struct.unpack_from('<H',b,o+2)[0],o+4) if v&32768 else (v,o+2)
 out=[]
 for i in range(count):
  o=p+start+struct.unpack_from('<I',b,p+h+i*4)[0]
  if flags&256:_,o=l8(o);n,o=l8(o);s=b[o:o+n].decode('utf-8')
  else:n,o=l16(o);s=b[o:o+2*n].decode('utf-16le')
  out.append(s)
 return out

def remove_ouya_category(raw):
 names=strings(raw);out=bytearray(raw[:8]);p=8;skip=0;removed=0
 while p<len(raw):
  typ,head,size=struct.unpack_from('<HHI',raw,p)
  if skip:
   if typ==0x102:skip+=1
   if typ==0x103:skip-=1
  else:
   remove=False
   if typ==0x102:
    name=struct.unpack_from('<I',raw,p+20)[0]
    ast,asz,ac=struct.unpack_from('<HHH',raw,p+24)
    if names[name]=='category':
     for i in range(ac):
      a=p+16+ast+i*asz
      key,value=struct.unpack_from('<II',raw,a+4)
      if names[key]=='name' and value!=0xffffffff and names[value]=='tv.ouya.intent.category.APP':remove=True
   if remove:skip=1;removed+=1
   else:out+=raw[p:p+size]
  p+=size
 if skip or removed!=1:raise ValueError(('Unexpected manifest structure',removed,skip))
 struct.pack_into('<I',out,4,len(out));return bytes(out)

def repackage(source,destination,manifest=None):
 with zipfile.ZipFile(source) as a,zipfile.ZipFile(destination,'w') as b:
  for info in a.infolist():
   if info.filename.upper().startswith('META-INF/'):continue
   data=a.read(info.filename)
   if info.filename=='AndroidManifest.xml':data=manifest if manifest is not None else remove_ouya_category(data)
   b.writestr(info,data)

if __name__=='__main__':
 repackage(sys.argv[1],sys.argv[2]);print('Launcher category corrected:',sys.argv[2])
