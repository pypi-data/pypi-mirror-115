import requests
from bs4 import BeautifulSoup
class Destiny(object):
    def __init__(self, BaseUrl) -> None:
        if BaseUrl.endswith("/"):
            self.BaseUrl = BaseUrl[:-1]
        else:
            self.BaseUrl = BaseUrl
        self.browser = requests.Session()
        self.browser.get(f"{self.BaseUrl}/")
    def Login(self, userName, password):
        self.browser.post(f"{self.BaseUrl}/district/servlet/handledistrictloginform.do", data={
        "loginName": userName,
        "password": password
    })

    def __parseCopyStatus(self, htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')

        # Basic Info
        title_link = soup.select("a.TitleLink")[0]
        title_text = title_link.get_text().strip()
        basic_info_table = soup.find(id="CopyInformationDetail_0")
        basic_info_table_rows = basic_info_table.find_all('tr')
        basic_info = {}
        basic_info["Title"] = title_text
        for row in basic_info_table_rows:
            header = row.select("td.SmallColHeading")[0].get_text()
            value = row.select('td[align="left"].ColRow')[0].get_text()
            
            header = header.replace('\xa0', "")
            value = value.replace('\xa0', "")
            basic_info[header] = value

        # Current Checkout
        current_checkout_table = soup.select("#currentCheckoutTable")[0]
        current_checkout = {}
        for row in current_checkout_table.find_all('tr'):
            header_td = row.select("td.SmallColHeading")
            if(len(header_td) > 0):
                header = header_td[0].get_text().strip()
                value = row.select('td.ColRow')[0].get_text().strip()
                header = header.replace('\xa0', "")
                value = value.replace('\xa0', "")
                current_checkout[header] = value
            else:
                current_checkout["Patron"] = "None"
        
        # Previous Checkout
        previous_checkout_table = soup.select("#previousCheckoutTable")[0]
        previous_checkout = {}
        for row in previous_checkout_table.find_all('tr'):
            header_td = row.select("td.SmallColHeading")
            if(len(header_td) > 0):
                header = header_td[0].get_text().strip()
                value = row.select('td.ColRow')[0].get_text().strip()
                header = header.replace('\xa0', "")
                value = value.replace('\xa0', "")
                previous_checkout[header] = value
            else:
                previous_checkout["Patron"] = "None"

        
        # notes
        notes_table = soup.select("#tableNotes")[0]
        notes = []
        rows = notes_table.find_all('tr')
        rows = rows[1::]
        for row in rows:
            notes.append(row.get_text().strip())
        
        final = {
            "Basic Information": basic_info,
            "Current Checkout": current_checkout,
            "Previous Checkout": previous_checkout,
            "Notes": notes
        }

        return final

    def get_copy_status(self, barcode):
        res = self.browser.post(f"{self.BaseUrl}/circulation/servlet/handlecopystatusform.do", data={
            "searchString": barcode
        })

        return self.__parseCopyStatus(res.text)

    
    def add_note(self, noteText, urgent="off"):
        res = self.browser.post(f"{self.BaseUrl}/circulation/servlet/handleaddeditcopynoteform.do", data={
            "urgent": urgent,
            "note": noteText,
            "saveNote.x": 27,
            "saveNote.y": 15
        })