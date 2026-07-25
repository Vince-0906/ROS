import threading
import requests

class Download:
    def download(self, url,callback_word_count):
        print(f'线程:{threading.get_ident()}开始下载:{url}')
        response =requests.get(url)
        response.encoding = 'utf-8'
        callback_word_count(url,response.text) #调用回调函数


    def start_download(self,url,callback_word_count):
        #self.download(url,callback_word_count)
        thread= threading.Thread(target=self.download,args=(url,callback_word_count))
        thread.start()

def word_count(url,reesult):
    """
    普通函数,用于回调,统计下载结果的长度,并打印前5个字符
    """
    print(f"{url}:{len(reesult)}->{reesult[:5]}")


def main():
    download =Download()
    download.start_download("https://www.shuyous.com/book/2468315-2139.html",word_count)
    download.start_download("https://www.shuyous.com/book/2468315-2135.html",word_count)
    download.start_download("https://www.shuyous.com/book/2468315-80.html",word_count)
