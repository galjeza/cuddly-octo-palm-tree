abeceda = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
rabiHeadless = "";
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}
imenaSlik = []
znamka = ""
pathToProfile = ""
novoOkno = None

#asd





def login(email, password):

    print("=> Prijavljam se v avto.net")
    time.sleep(10)
    try:
        driver.find_element_by_id("CybotCookiebotDialogBodyLevelButtonAccept").click()
    except:
        print("...")

    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, "enaslov")))
    driver.execute_script("document.getElementsByName('enaslov')[0].value='" + email + "'")
    time.sleep(1)
    try:
        driver.find_element_by_id("CybotCookiebotDialogBodyLevelButtonAccept").click()
    except:
        print("...")

    box2 = driver.find_element_by_xpath("//input[@type='password']")
    box2.click()
    box2.clear()
    box2.send_keys(password)
    time.sleep(3)
    pravnoobvestilo = driver.find_element_by_id('pravnoobvestilo')
    driver.execute_script("arguments[0].click();", pravnoobvestilo)
    driver.execute_script("arguments[0].click();", driver.find_element_by_name("LOGIN"))
    time.sleep(2)
    WebDriverWait(driver, 10000).until(ec.visibility_of_element_located((By.CLASS_NAME, "mojtrg")))
    print("=> prijavljen v avto.net ")
    


def pojdiNaUredi(url):
           
    print("=> Pridobivam slike oglasa")
    driver.get(url)
    try:
        left = "id="
        right = "&"
        id = url[url.index(left) + len(left):url.index(right)]
        urediUrl = "https://www.avto.net/_2016mojavtonet/ad_edit.asp?id=" + id
    except:
        id = url.split("id=")[1]
        urediUrl = "https://www.avto.net/_2016mojavtonet/ad_edit.asp?id=" + id

    kilometri = WebDriverWait(driver, 30).until(
        ec.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/small/div[1]/div[2]/div/div[7]/div[2]")))
    kilometri = kilometri.text.strip()
    kilometri = re.sub('[^A-Za-z0-9]+', '', kilometri)
    imeAvta = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/h1").text.strip()

    imeAvta = re.sub('[^A-Za-z0-9]+', '', imeAvta)
    slikeElements = driver.find_elements_by_tag_name("p")
    i = 1
    for slika in slikeElements:
        urlSlike = slika.get_attribute("data-src")
        if urlSlike != None:
            filename = "avtonetdata/slikeAvta/" + abeceda[i] + kilometri + imeAvta + ".png"
            if path.exists(filename) == False:
                r = requests.get(urlSlike, headers=headers, stream=True,verify="")
                im = Image.open(BytesIO(r.content))
                im = im.filter(ImageFilter.SMOOTH_MORE)
                im.save(filename, quality=95, subsampling=0)
                i = i + 1
                print("=> shranil sem: " + abeceda[i] + kilometri + imeAvta + ".png")
                imenaSlik.append(filename)
            else:
                print("=> slika je že shranjena na računalniku")
                imenaSlik.append(filename)
                i = i + 1
    print("=> slike oglasa pridobljene ")
    driver.get(urediUrl)


def ustvariNovOglasStran():
    global znamka
    print("=> ustvarjam nov oglas")
    driver.execute_script("window.open('https://www.avto.net/_2016mojavtonet/ad_select_rubric_icons.asp?SID=10000');")
    global novOglasWindow
    novOglasWindow = driver.window_handles[driver.window_handles.index(originalOglasWindow)+1]
    driver.switch_to.window(novOglasWindow)
    try:
        driver.find_element_by_name("znamka")
    except:
        time.sleep(60 * 60)
        driver.get("https://www.avto.net/_2016mojavtonet/ad_select_rubric_icons.asp?SID=10000")
    try:
        Select(driver.find_element_by_name("znamka")).select_by_value(znamka)
        time.sleep(2)
    except:
        if (znamka == "Ssangyong"):
            znamka = "SsangYong"
        strippedZnamka = znamka.replace(" ", "")
        print(strippedZnamka)
        Select(driver.find_element_by_name("znamka")).select_by_value(strippedZnamka)

    try:
        print(model)
        Select(driver.find_element_by_name("model")).select_by_value(model)

    except Exception as e:
        print(e)
        try:
           errorModel = model.replace(" ","---")
           print(errorModel)
           Select(driver.find_element_by_name("model")).select_by_value(errorModel)
        except Exception as error:
           print(error)
           Select(driver.find_element_by_name("model")).select_by_value("modela ni na seznamu")
    time.sleep(1)
    Select(driver.find_element_by_name("oblika")).select_by_index(0)
    time.sleep(1)
    try:
        Select(driver.find_element_by_name("mesec")).select_by_value(mesReg)
    except:
        Select(driver.find_element_by_name("mesec")).select_by_value("10")

    time.sleep(1)
    try:
        Select(driver.find_element_by_name("leto")).select_by_visible_text(letoReg)
    except:
        Select(driver.find_element_by_name("leto")).select_by_visible_text("NOVO vozilo")
    time.sleep(1)
    driver.execute_script("arguments[0].click();",
                          driver.find_element_by_xpath("//*[contains(text(),'" + gorivo + "')]"))
    time.sleep(1)

    driver.find_element_by_name("potrdi").click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "supurl"))).click()


def pridobiPodatkeZaPrvoStran():
    print("=> pridobivam podatke o avtu")
    global znamka
    global model
    global letoReg
    global mesReg
    global gorivo
    znamka = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, "znamka"))).get_attribute(
        "value")

    model = driver.find_element_by_name("model").get_attribute("value")
    letoReg = driver.find_element_by_id("letoReg").get_attribute("value")
    select = Select(driver.find_element_by_id("mesReg"))
    mesReg = select.first_selected_option.text.strip()

    gorivo = driver.find_element_by_name("gorivo").get_attribute("value")
    
    if gorivo == "elektro pogon":
        gorivo = "e-pogon"
    if gorivo == "CNG plin":
        gorivo = "CNG zemeljski plin"
    if gorivo == "LPG plin":
        gorivo = "LPG avtoplin"

    print("=> osnovni podatki o avtu pridobljeni ")


def kopirajInPrilepiPodatke(url):
    print("=> kopiram vse podatke o avtu")
    driver.switch_to.window(originalOglasWindow)
    time.sleep(2)
    inputElements = driver.find_elements_by_xpath("//input[@type='text']")
    inputValues = []
    for input in inputElements:
        time.sleep(1)
        inputValues.append(input.get_attribute("value"))

    textAreaElements = driver.find_elements_by_tag_name("textarea")
    textValues = []
    for tekst in textAreaElements:
        textValues.append(tekst.text)
    selectElements = driver.find_elements_by_tag_name("select")
    selectValues = []
    time.sleep(3)
    for select in selectElements:
        time.sleep(1)
        selectedOption = Select(select).first_selected_option.text
        
        selectValues.append(selectedOption)

    checkedCheckboxes = []
    checkboxes = driver.find_elements_by_xpath("//input[@type='checkbox']")
    for checkbox in checkboxes:
        if checkbox.is_selected():
            checkedCheckboxes.append(checkbox.get_attribute("name"))
    print("=> vsi podatki o avtu kopirani ")

    try:
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        body = driver.find_element_by_xpath("/html/body")
        innerHTML = body.get_attribute("innerHTML").replace('"', '\\"')
        driver.switch_to.default_content();
    except:
        print("")
    # spremeni podatek zato da nebo isti oglas v arhivu
    randoma = str(random.randint(1998, 2021))
    time.sleep(2)

    randomc = str(int(float(driver.find_element_by_id("cena").get_attribute("value"))) + 500)

    randomb = str(random.randint(100000, 300000))
    driver.find_element_by_name("letoReg").click()
    driver.find_element_by_name("letoReg").clear()
    driver.find_element_by_name("letoReg").send_keys(randoma)
    time.sleep(1)
    driver.find_element_by_name("prevozenikm").click()
    driver.find_element_by_name("prevozenikm").clear()
    driver.find_element_by_name("prevozenikm").send_keys(randomb)
    time.sleep(1)
    driver.find_element_by_name("cena").click()
    driver.find_element_by_name("cena").clear()
    driver.find_element_by_name("cena").send_keys(randomc)
    time.sleep(1)
    driver.find_element_by_name("ADVIEW").click()

    driver.get(url)
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'odstrani oglas')]"))).click()
    WebDriverWait(driver, 10).until(ec.alert_is_present(), "")
    time.sleep(5)
    driver.switch_to.alert.accept()
    time.sleep(2)

    #########################################################################################################
    print("=> vstavljam podatke o avtu")
    driver.switch_to.window(novOglasWindow)
    time.sleep(1)
    try:
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        body = driver.find_element_by_xpath("/html/body")
        driver.execute_script('arguments[0].innerHTML = "' + innerHTML + '"', body)
        driver.switch_to.default_content()
    except:
        print("")

    newInputeElements = driver.find_elements_by_xpath("//input[@type='text']")
    for newElement in newInputeElements:
        try:
            newElement.click()
            newElement.clear()
            newElement.send_keys(inputValues[newInputeElements.index(newElement)])
            time.sleep(1)
        except Exception as e:

            continue

    newTextElements = driver.find_elements_by_tag_name("textarea")
    for newElement in newTextElements:
        try:
            newElement.click()
            newElement.clear()
            newElement.send_keys(textValues[newTextElements.index(newElement)])
            time.sleep(1)
        except Exception as  e:

            continue

    newSelects = driver.find_elements_by_tag_name("select")
    for n in newSelects:
        try:
           
           selectedOption = selectValues[newSelects.index(n)]
           driver.execute_script("arguments[0].scrollIntoView();", n)
           n.click()
           time.sleep(1) 
           Select(n).select_by_visible_text(selectedOption)
           time.sleep(1)   
        except Exception as  e:
            print("SELECT ERR")
            continue
                                 
        

    for checkbox in checkedCheckboxes:
        newCheckBox = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.NAME, checkbox)))
        if newCheckBox.is_selected() != True:
            try:
                newCheckBox.click()
                time.sleep(1)
            except:
                try:
                    driver.execute_script("arguments[0].click();", newCheckBox)
                    time.sleep(1)
                except:
                    newCheckBox.send_keys(Keys.SPACE)
                    time.sleep(1)
    try:
         porabaOBJAVI = driver.find_element_by_name("porabaOBJAVI")
         if porabaOBJAVI.is_selected():
             porabaOBJAVI.click() 
    except:
           print("e")
   
    print("=> podatki vstavljeni v nov oglas ")


def dodajSlike():
    print("=> dodajam slike")
    dodajslikebtn = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'OBJAVI OGLAS + uredi fotografije')]")))
    dodajslikebtn.click()
    n = 0
    global imenaSlik
    imenaSlik.sort()
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[3]/a/strong"))).click()
    except:
        print("")
    time.sleep(5)
    try:
        driver.find_element_by_xpath(
            "//*[text()='Ali bi raje fotografije objavili 1 po 1, posamično? Kliknite tukaj za posamično dodajanje fotografij.']").click()
        for imeDatoteke in imenaSlik:
            if imeDatoteke.endswith(".png"):
                celoIme = os.path.abspath(imeDatoteke)
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.NAME, "fotografija"))).clear()
                driver.find_element_by_name("fotografija").send_keys(celoIme)
                driver.find_element_by_name("gumb" + str(n + 1)).click()
                n = n + 1
                time.sleep(1)

    except:
        for imeDatoteke in imenaSlik:
            if imeDatoteke.endswith(".png"):
                celoIme = os.path.abspath(imeDatoteke)
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.NAME, "fotografija"))).clear()
                driver.find_element_by_name("fotografija").send_keys(celoIme)
                driver.find_element_by_name("gumb" + str(n + 1)).click()
                n = n + 1

    print("=> slike so dodane ")
    driver.find_element_by_xpath("//*[contains(text(), 'Zaključi urejanje')]").click()


def zbrisiOriginalniOglas(url):
    print("=> brišem prvotni oglas")
    driver.get(url)
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'odstrani oglas')]"))).click()
    WebDriverWait(driver, 10).until(ec.alert_is_present(), "")
    time.sleep(5)
    driver.switch_to.alert.accept()
    time.sleep(2)

    print("=> prvotni oglas je izbrisan ")


def zapriBrowser():
    global imenaSlik
    imenaSlik = []


def pokaziPopup():
    tk.messagebox.showinfo("Opozorilo",
                           "Program bo izbrisal oglas/e med procesom ne uporabljajte miške ali \n tipkovnice  in počakajte da se brskalnik samostojno vgasne.", )


def main():
    pause = int(pauseEntry.get())
    print("=")
    urlji = []
    root.withdraw()
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--disable-web-security");
    chrome_options.add_argument("--allow-running-insecure-content");
    if(rabiHeadless=="NE"):
        chrome_options.add_argument("--headless")

    chromeVersion = "114.0.5735.16"
    if(email == "dlcavto@gmail.com" or email=="avtomedvode@gmail.com" ):
        chromeVersion = "109.0.5414.25"
    if(email == "meglic.zdenko@gmail.com"):
        chromeVersion = "103.0.5060.134"           
               
                      

    driver = webdriver.Chrome(ChromeDriverManager(version=chromeVersion).install(), chrome_options=chrome_options)
    print("=> vsi gonilniki uspešno pridobljeni")

    driver.get("https://www.avto.net/_2016mojavtonet/")
    driver.maximize_window()
    global originalOglasWindow
    originalOglasWindow = driver.current_window_handle
    try:
        login(email, geslo)
         
    except:
        WebDriverWait(driver, 10000).until(ec.visibility_of_element_located((By.NAME, "enaslov")))
        login(email, geslo)

    #get href of the parent element of element with class "mojtrg"
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "mojtrg")))
    mojtrg = driver.find_element_by_class_name("mojtrg")
    mojtrgParent = mojtrg.find_element_by_xpath("..")
    mojtrgHref = mojtrgParent.get_attribute("href")

    broker = mojtrgHref.split("broker=")[1].split("&")[0]
    

   
    
    
    for i in range(1,3):
        try:
            driver.get("https://www.avto.net/_2016mojavtonet/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=0&mocMax=999999&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000001000&EQ7=1110100120&EQ8=101000000&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PIAOut=&PSLO=&akcija=0&paketgarancije=&broker="+str(broker)+"&prikazkategorije=0&kategorija=0&ONLvid=0&ONLnak=0&zaloga=10&arhiv=0&presort=1&tipsort=ASC&stran="+str(i)+"&subSORT=3&subTIPSORT=ASC")    
            time.sleep(2)          
            WebDriverWait(driver, 10000).until(ec.visibility_of_element_located((By.CLASS_NAME, "mojtrg")))
            driver.get("https://www.avto.net/_2016mojavtonet/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=0&mocMax=999999&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000001000&EQ7=1110100122&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker="+str(broker) +"&prikazkategorije=0&kategorija=0&ONLvid=0&ONLnak=0&zaloga=10&arhiv=0&presort=1&tipsort=ASC&stran="+str(i)+"&subSORT=3&subTIPSORT=ASC")                
            WebDriverWait(driver, 10000).until(ec.visibility_of_element_located((By.CLASS_NAME, "ResultsMenuBoxnazivTrgovec")))

            time.sleep(5)
            total_height = int(driver.execute_script("return document.body.scrollHeight"))

            for i in range(1, total_height, 5):
                driver.execute_script("window.scrollTo(0, {});".format(i))
            time.sleep(5)
            results = driver.find_elements_by_class_name("ResultsAd")
            for result in results:
                try:
            
                    try:
                        result.find_element_by_class_name("ResultsAdPriceRegular")   
                    except:
                        result.find_element_by_class_name("ResultsAdPriceAkcijaCena")
                    urlji.append(result.find_element_by_class_name("Adlink").get_attribute("href"))
                except:
                    print("Avto je že prodan")
        except:
            print("Na tej strani ne najdem oglasov")
        

   
    print(urlji)
    for url in urlji:
        urlOglasa = url
        pojdiNaUredi(urlOglasa)
        pridobiPodatkeZaPrvoStran()
        ustvariNovOglasStran()
        kopirajInPrilepiPodatke(urlOglasa)
        dodajSlike()
        time.sleep(2)
        zapriBrowser()
        driver.close()
        driver.switch_to.window(originalOglasWindow)
        print("Obnovil sem toliko oglasov:" + str(urlji.index(url) + 1))
        time.sleep(pause * 60)

    print(">>>PROCES USPEŠNO ZAKLJUČEN<<<")
    time.sleep(3)
    driver.quit()
    root.deiconify()


print("=> program se zaganja...")
root = tk.Tk()
root.iconbitmap("avtonetdata/img/logo.ico")
root.title("AvtoNetBot v4")
canvas1 = tk.Canvas(root, width=600, height=300, relief='raised')
image = ImageTk.PhotoImage(Image.open("avtonetdata/img/tkinterozadje.jpg"))
canvas1.create_image(0, 0, anchor=tk.NW, image=image)
canvas1.pack()
label2 = tk.Label(root, text='Premor med oglasi(min):')
label2.config(font=('helvetica', 9))
canvas1.create_window(395, 240, window=label2)
pauseEntry = tk.Entry(root)
canvas1.create_window(530, 240, window=pauseEntry)

button1 = tk.Button(text='Izbriši in ponovno ustvari vse oglase', command=lambda: [main()], bg='white', fg='black',
                    font=('helvetica', 10, 'bold'))
canvas1.create_window(467, 270, window=button1)
if os.path.getsize("avtonetdata/mailgeslo.txt") == 0:
    email = simpledialog.askstring("Prva uporaba programa", "vnesite email naslov za avto.net")
    geslo = simpledialog.askstring("Prva uporaba programa", "vnesite geslo za avto.net")
    f = open("avtonetdata/mailgeslo.txt", "w")
    f.write(email)
    f.write("\n")
    f.write(geslo)
    f.close()

email = ""
geslo = ""
gesloinime = []
with open("avtonetdata/mailgeslo.txt", "r") as file:
    for line in file:
        gesloinime.append(line.strip())
email = gesloinime[0]
geslo = gesloinime[1]

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("avtonetdata/creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("avtonetbot dostop").sheet1  # Open the spreadhseet

try:
    
    emailRow = sheet.find(email).row
    print("Email najden v podatkovni bazi.")
    placanoCell = sheet.cell(emailRow, 2).value.strip()
    rabiHeadless = sheet.cell(emailRow,10).value.strip()
    print("$$")
    if placanoCell == "NE":
        print("NISTE NAROČENI NA PROGRAM!")
        print("ZA NAKUP PROGRAMA PIŠITE NA gal.jeza@protonmail.com")
        print("ČE STE NAROČENI NA PROGRAM IN VSEENO VIDITE TO SPOROČILO ME KONTAKTIRAJTE")
    else:
        print("€€")
        usage = sheet.cell(emailRow,3).value.strip()
        usage = int(usage) +1
        sheet.update_cell(emailRow,3,str(usage))

        root.mainloop()
except(err):
    print(err)
    print("google sheets eroor")
    print("NISTE NAROČENI NA PROGRAM!")
    print("ZA NAKUP PROGRAMA PIŠITE NA gal.jeza@protonmail.com")
    print("ČE STE NAROČENI NA PROGRAM IN VSEENO VIDITE TO SPOROČILO ME KONTAKTIRAJTE")
    time.sleep(30)
