import requests
import bs4

"""
Get ISIN CODE from KRX
"""
def getIsinCode(stock_name):
    url = "http://marketdata.krx.co.kr/WEB-APP/autocomplete/autocomplete.jspx?contextName=stkisu3&value="
    r = requests.get(url + stock_name)
    
    doc = bs4.BeautifulSoup(r.text, "html5lib")
    isu_cd = doc.find('li')['data-cd']
    isu_srt_cd = doc.find('li')['data-tp']
    return isu_cd, isu_srt_cd
    
    
if __name__ == '__main__':
    isu_cd, isu_srt_cd = getIsinCode("에넥스")
    print (isu_cd, isu_srt_cd)
        
        
        
        