import requests
import requests.exceptions
import os
import codecs
import threading
import queue

class process_one_url(threading.Thread):
    def __init__(self, host, q, tid):
        threading.Thread.__init__(self)
        self.host = host
        self.q=q
        self.tid=tid

    def run(self):
        while True:
            try:
                fname=self.q.get(False)
                if fname==None:
                    print(str(self.tid)+': quit')
                    break
                url=host+fname
                print(str(self.tid)+':'+url)
                while True:
                    try:
                        html=requests.get(url)
                        break
                    except requests.ConnectionError:
                        print(str(self.tid)+': ConnectionError')
                    except requests.exceptions.ChunkedEncodingError:
                        print(str(self.tid)+': ChunkedEncodingError')
                    except Exception as ex:
                        print('{0}: request.get() exception ({1}) occurred.'.format(self.tid, type(ex).__name__))
                fw=codecs.open(fname,'w','utf-8')
                fw.write(html.text)
                fw.close()
            except queue.Empty:
                print(str(self.tid)+': quit')
                break
            except Exception as ex:
                print('{0}: An exception ({1}) occurred.'.format(self.tid, type(ex).__name__))
        
def download_tianya_page(pageurl):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'Accept': 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'en-CA,en;q=0.8,en-GB;q=0.6,en-US;q=0.4,zh-CN;q=0.2,zh;q=0.2'}
    html = requests.get(pageurl, headers)
    return html

if __name__ == '__main__':
    exit(0)
dirname='tianya'
try:
    os.mkdir(dirname)
except FileExistsError:
    print('folder '+dirname+' already exist')
os.chdir(dirname)

q=queue.Queue()
host='http://bbs.tianya.cn/'
for i in range(1,531):
    fname ='post-free-3077648-{0}.shtml'.format(i)
    print(fname)
    q.put(fname)

t=[]
for i in range(10):
    t.append(process_one_url(host, q, i))
    t[i].start()
for i in range(10):
    t[i].join()

print('finished')
