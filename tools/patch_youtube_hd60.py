import pathlib,zipfile,struct,hashlib,zlib,shlex,json
import argparse
p=argparse.ArgumentParser(description='Parche experimental local para YouTube OUYA HD60')
p.add_argument('--input',required=True,type=pathlib.Path)
p.add_argument('--output',default='build',type=pathlib.Path)
a=p.parse_args()
ROOT=a.output
ROOT.mkdir(parents=True,exist_ok=True)
EXPECTED='1a91a635aa8e769e86d683dcbff86e1508b7f7d6f2fb308f17666bcdf43b671b'
if hashlib.sha256(a.input.read_bytes()).hexdigest()!=EXPECTED:raise SystemExit('La APK original no coincide con la version probada')
OLD='tv.ouya.youtube';NEW='tv.ouya.youtubb'
UA='Mozilla/5.0 (Linux; Android 4.1.2;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36, OUYA Console Build/JZO54L-OUYA, OUYA/1.0.10 (OUYA, JZO54L-OUYA, Wireless) (PS4; Leanback Shell)'
def uleb(b,o):
 n=s=0
 while True:
  v=b[o];o+=1;n|=(v&127)<<s
  if v<128:return n,o
  s+=7
def enculeb(n):
 b=bytearray()
 while n>=128:b.append((n&127)|128);n>>=7
 b.append(n);return bytes(b)
def patch_dex(raw):
 b=bytearray(raw);count,table=struct.unpack_from('<II',b,56);strings=[];changed=[]
 for i in range(count):
  off=struct.unpack_from('<I',b,table+i*4)[0];n,start=uleb(b,off);end=b.index(0,start);s=bytes(b[start:end]).decode('utf-8',errors='replace');new=None
  if s.startswith('content_shell chrome --js-flags='):
   # Retain existing rendering/GPU switches; remove diagnostic logging to fit
   # the new options in the original DEX allocation without moving sections.
   remove=['--v=1','--vmodule=chunk*=1,source*=1,media*=1,webmed*=1,*=0','--webcore-log-channels=Media','--enable-dcheck','--enable-accelerated-scrollable-frames','--enable-composited-scrolling-for-frames','--enable-begin-frame-scheduling','--enable-deadline-scheduling','--ui-prioritize-in-gpu-process','--profiler-timing=0']
   new=s
   for x in remove:new=new.replace(' '+x,'')
   new += ' --disable-opus-playback --user-agent="'+UA+'"'
  elif s==OLD:new=NEW
  if new is not None:
   new=new.ljust(n,' ')
   data=enculeb(len(new))+new.encode()+b'\0';space=end+1-off
   if len(data)>space:raise ValueError(('DEX allocation exceeded',len(data),space))
   b[off:end+1]=data+b'\0'*(space-len(data));changed.append({'index':i,'old':s,'new':new})
  strings.append((new if new is not None else s))
 # Compare original/new ordering only for modified ASCII entries.
 for c in changed:
  i=c['index'];assert strings[i-1]<=strings[i]<=strings[i+1],('String order',i)
 assert len(changed)==2,changed
 b[12:32]=hashlib.sha1(b[32:]).digest();struct.pack_into('<I',b,8,zlib.adler32(b[12:])&0xffffffff)
 return bytes(b),changed

def axml(raw):
 b=bytearray(raw);pos=8;patches=[]
 while pos<len(b):
  typ,head,size=struct.unpack_from('<HHI',b,pos)
  if typ==1:break
  pos+=size
 count,stylecount,flags,start,stylestart=struct.unpack_from('<5I',b,pos+8)
 assert not stylecount and not stylestart
 utf8=bool(flags&256);ss=[]
 def len8(o):
  v=b[o];return (((v&127)<<8)|b[o+1],o+2) if v&128 else (v,o+1)
 def len16(o):
  v=struct.unpack_from('<H',b,o)[0];return (((v&32767)<<16)|struct.unpack_from('<H',b,o+2)[0],o+4) if v&32768 else (v,o+2)
 for i in range(count):
  o=pos+start+struct.unpack_from('<I',b,pos+head+i*4)[0]
  if utf8:_,o=len8(o);n,o=len8(o);s=bytes(b[o:o+n]).decode('utf-8')
  else:n,o=len16(o);s=bytes(b[o:o+2*n]).decode('utf-16le')
  ss.append(s)
 old=ss[:]
 for i,s in enumerate(ss):
  if s==OLD:ss[i]=NEW
  elif s in ['YouTubeActivity','YouTubeApplication']:ss[i]=OLD+'.'+s
  elif s=='org.chromium.content_shell.permission.SANDBOX':ss[i]=NEW+'.permission.SANDBOX'
 titleidx=len(ss);ss.append('YouTube OUYA HD60')
 # Change only application label to an inline string, preserving resources.
 p=pos+size
 while p<len(b):
  t,h,n=struct.unpack_from('<HHI',b,p)
  if t==0x102:
   name=struct.unpack_from('<I',b,p+20)[0];ast,asz,ac=struct.unpack_from('<HHH',b,p+24)
   if old[name]=='application':
    for i in range(ac):
     a=p+16+ast+i*asz;key=struct.unpack_from('<I',b,a+4)[0]
     if old[key]=='label':struct.pack_into('<I',b,a+8,titleidx);b[a+15]=3;struct.pack_into('<I',b,a+16,titleidx)
  p+=n
 def lenbytes(n):
  return bytes([(n>>8)|128,n&255]) if n>127 else bytes([n])
 data=bytearray();offsets=[]
 for s in ss:
  offsets.append(len(data));v=s.encode('utf-8' if utf8 else 'utf-16le')
  data+=(lenbytes(len(s))+lenbytes(len(v)) if utf8 else struct.pack('<H',len(s)))+v+(b'\0' if utf8 else b'\0\0')
 while len(data)%4:data+=b'\0'
 newstart=head+4*len(ss);newsize=newstart+len(data)
 pool=struct.pack('<HHI5I',1,head,newsize,len(ss),0,flags&~1,newstart,0)+b''.join(struct.pack('<I',x) for x in offsets)+data
 assert head==28
 result=b[:pos]+pool+b[pos+size:];struct.pack_into('<I',result,4,len(result))
 return result
with zipfile.ZipFile(a.input) as zin:
 dex,changes=patch_dex(zin.read('classes.dex'));manifest=axml(zin.read('AndroidManifest.xml'))
 with zipfile.ZipFile(ROOT/'youtube-hd60-unsigned.apk','w',compression=zipfile.ZIP_DEFLATED) as zout:
  for info in zin.infolist():
   if info.filename.upper().startswith('META-INF/'):continue
   data= dex if info.filename=='classes.dex' else manifest if info.filename=='AndroidManifest.xml' else zin.read(info.filename)
   zout.writestr(info,data)
(ROOT/'Cambios-tecnicos-HD60.json').write_text(json.dumps({'package':NEW,'changes':changes},indent=2),encoding='utf-8')
print('Clone construido:',NEW)



