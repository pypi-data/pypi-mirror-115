# python读取剪切板内容
import win32clipboard as w
import win32con

def getText():
    try:
        w.OpenClipboard()
        d = w.GetClipboardData(win32con.CF_TEXT)
        w.CloseClipboard()
        return(d).decode('GBK')
    except:
        return None

def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()

if __name__ =='__main__':
    print(getText())