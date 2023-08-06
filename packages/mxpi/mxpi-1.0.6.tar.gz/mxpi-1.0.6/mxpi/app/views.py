from django.shortcuts import render
from django.contrib.auth.backends import UserModel
from django.shortcuts import render
from django.http import HttpResponse, request, response
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import reverse,redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from MxPisite import settings
from django.utils import timezone
import subprocess,sys,mxpi,os,json,time
from app import models
import threading
import requests
import base64


# Create your views here.
def home(request):
    return render(request,'index.html')

def upfile(request):
    code = request.POST.get('code')
    f=open(os.path.dirname(mxpi.__file__)+'/file/test.py','w',encoding='utf-8')
    #f=open('file/test.py','w')
    f.write(code)
    f.close()
    return HttpResponse('ok')

def cmd_msg(request):
    datas=models.MxpiArticles.objects.filter(read=0)
    if len(datas)>0:
        datas[0].read=1
        datas[0].save()
        print(datas[0].body)
        return HttpResponse(datas[0].body)
    else:
        return HttpResponse('cmd')

def run_cmd(request):
    models.MxpiArticles.objects.filter(title='cmd').delete()
    p = subprocess.Popen('python -u file/test.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=1)
    while p.poll() is None:
            #sys.stdout.flush()
            line = p.stdout.readline().strip()
            if line:
                line = _decode_data(line)
                print(line)
                #s=myThread(line)
                #s.start()
    return HttpResponse('ok')

class myThread (threading.Thread):
    def __init__(self, line):
        threading.Thread.__init__(self)
        self.line = line
    def run(self):
        models.MxpiArticles.objects.create(title='cmd',body=self.line,read=False)

def _decode_data(byte_data: bytes):
    """
    解码数据
    :param byte_data: 待解码数据
    :return: 解码字符串
    """
    try:
        return byte_data.decode('UTF-8')
    except UnicodeDecodeError:
        return byte_data.decode('GB18030')

def file_list(request):
    url_=os.path.dirname(mxpi.__file__).replace('\\','/')
    url=url_+'/static/file'
    dirs=os.listdir(url)
    s=[]
    id=0
    for f in dirs:
        id += 1
        f_i={'id':'','name':'',"size":'','url':'','last':''}
        size=os.path.getsize(url+'/'+f)
        f_i['id']=id
        f_i['name']=f
        f_i['size']='%.2f' % float(size/1000) + 'KB'
        f_i['url']=url+'/'+f
        f_i['url_g']='/static/file/'+f
        f_i['last']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(url+'/'+f).st_mtime))
        s.append(f_i)
    data={
        'msg':'ok',
        'data':s,
    }
    return HttpResponse(json.dumps(data))

def file_remove(request):
    data=request.GET.get('data')
    os.remove(data)
    return HttpResponse('ok')

def files(request):
        file_obj = request.FILES.get('avatar')
        if file_obj.name=='blob':
            with open(os.path.dirname(mxpi.__file__)+'/static/file/sound'+str(int(time.time()))+'.wav', "wb") as f:
                    for line in file_obj:
                        f.write(line)
            return HttpResponse('ok')
        else:
            with open(os.path.dirname(mxpi.__file__)+'/static/file/'+file_obj.name, "wb") as f:
                for line in file_obj:
                    f.write(line)
            return HttpResponse('ok')
 
def get_c(request):
    try:
        name=request.GET.get('name')
        file='example/'+name+'.mxpi'
        print(file)
        if os.path.exists(file):
            f=open(file,'r',encoding='utf-8')
            c=f.read()
            return HttpResponse(json.dumps({'msg':'ok','data':c}))
        else:
            return HttpResponse(json.dumps({'msg':'err','data':''}))
    except:
         return HttpResponse(json.dumps({'msg':'err','data':''}))


def read_model_list(request):
    try:
        rq = requests.get('http://120.79.209.170/getList')
        rq.encoding='utf-8'
        return HttpResponse(json.dumps({'msg':'ok','data':rq.json()}))
    except:
        print('无法连接网络数据库,请确定设备是否联网。')
        return HttpResponse(json.dumps({'msg':'err','data':'无法连接网络数据库,请确定设备是否联网。'}))
    
def get_upmodel(request):
    name=request.GET.get('name')
    filetype=request.GET.get('type')
    info=request.GET.get('info')
    people=request.GET.get('fp_people')
    files = { 
    "field1" : (name,open(os.path.dirname(mxpi.__file__)+'/static/file/'+name,"rb"),filetype),
    } 
    rq = requests.post(url='http://120.79.209.170/upfile_Ajax',files=files,params={'name':name,'type':filetype,'info':info,'people':people})
    rq.encoding='utf-8'
    print(rq.text)
    return HttpResponse(rq.text)

def downModel(request):
    id=request.GET.get('id')
    name=request.GET.get('name')
    r = requests.get('http://120.79.209.170/downfile_Ajax',params={'id':id}) # 发送请求
    with open (os.path.dirname(mxpi.__file__)+'/static/file/'+name, 'wb') as f:
        f.write(r.content)
        f.close
    return HttpResponse('ok')    
