

abeceda = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
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



def login(email, password):
    print("=> Prijavljam se v avto.net")
    box = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.NAME, "enaslov")))
    driver.execute_script("document.getElementsByName('enaslov')[0].value='"+email+"'")

    box2 = driver.find_element_by_xpath("//input[@type='password']")
    box2.click()
    box2.clear()
    box2.send_keys(password)
    time.sleep(3)
    pravnoobvestilo = driver.find_element_by_id('pravnoobvestilo')
    driver.execute_script("arguments[0].click();", pravnoobvestilo)
    driver.execute_script("arguments[0].click();", driver.find_element_by_name("LOGIN"))

    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "mojtrg")))
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

    kilometri = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/small/div[1]/div[2]/div/div[7]/div[2]")))
    kilometri = kilometri.text.strip()
    kilometri = re.sub('[^A-Za-z0-9]+', '', kilometri)
    imeAvta = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div[2]/h1").text.strip()
    imeAvta = re.sub('[^A-Za-z0-9]+', '', imeAvta)
    slikeElements = driver.find_elements_by_tag_name("p")
    i = 1
    for slika in slikeElements:
        urlSlike = slika.get_attribute("data-src")
        if urlSlike != None:
            filename = "avtonetdata/slikeAvta/" + abeceda[i] + kilometri + imeAvta + ".png"
            if path.exists(filename) == False:
                r = requests.get(urlSlike, headers=headers, stream=True)
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
    print("=> ustvarjam nov oglas")
    driver.execute_script("window.open('https://www.avto.net/_2016mojavtonet/ad_select_rubric_icons.asp?SID=10000');")
    global novOglasWindow
    novOglasWindow = driver.window_handles[1]
    driver.switch_to.window(novOglasWindow)
    try:
        Select(driver.find_element_by_name("znamka")).select_by_value(znamka)
    except:
        strippedZnamka = znamka.replace(" ","")
        print(strippedZnamka)
        Select(driver.find_element_by_name("znamka")).select_by_value(strippedZnamka)

    try:
        Select(driver.find_element_by_name("model")).select_by_value(model)
    except:
        Select(driver.find_element_by_name("model")).select_by_value("modela ni na seznamu")
    Select(driver.find_element_by_name("oblika")).select_by_index(0)
    Select(driver.find_element_by_name("mesec")).select_by_value(mesReg)
    Select(driver.find_element_by_name("leto")).select_by_visible_text(letoReg)
    driver.find_element_by_xpath("//*[contains(text(),'"+gorivo+"')]").click()
    driver.find_element_by_name("potrdi").click()
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
    print("=> osnovni podatki o avtu pridobljeni ")


def kopirajInPrilepiPodatke(url):
    print("=> kopiram vse podatke o avtu")
    driver.switch_to.window(originalOglasWindow)
    time.sleep(2)
    inputElements = driver.find_elements_by_xpath("//input[@type='text']")
    inputValues  = []
    for input in inputElements:
        time.sleep(1)
        inputValues.append(input.get_attribute("value"))

    textAreaElements = driver.find_elements_by_tag_name("textarea")
    textValues= []
    for tekst in textAreaElements:
        textValues.append(tekst.text)
    selectElements = driver.find_elements_by_tag_name("select")
    selectValues = []
    for select in selectElements:
        selectedOption = Select(select).first_selected_option.get_attribute("value")
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
        innerHTML = body.get_attribute("innerHTML").replace('"','\\"')
    except:
        print("")
    #spremeni podatek zato da nebo isti oglas v arhivu
    randoma = str(random.randint(1998, 2021))
    randomb = str(random.randint(1000, 500000))
    randomc = str(random.randint(1000, 10000))
    driver.find_element_by_name("letoReg").click()
    driver.find_element_by_name("letoReg").clear()
    driver.find_element_by_name("letoReg").send_keys(randoma)
    driver.find_element_by_name("prevozenikm").click()
    driver.find_element_by_name("prevozenikm").clear()
    driver.find_element_by_name("prevozenikm").send_keys(randomb)
    driver.find_element_by_name("cena").click()
    driver.find_element_by_name("cena").clear()
    driver.find_element_by_name("cena").send_keys(randomc)
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
        except Exception as e:
            
            continue

    newTextElements= driver.find_elements_by_tag_name("textarea")
    for newElement in newTextElements:
        try:
            newElement.click()
            newElement.clear()
            newElement.send_keys(textValues[newTextElements.index(newElement)])
        except Exception as  e:
            
            continue

    newSelects = driver.find_elements_by_tag_name("select")
    for n in newSelects:
        Select(n).select_by_value(selectValues[newSelects.index(n)])

    for checkbox in checkedCheckboxes:
        newCheckBox = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.NAME, checkbox)))
        if newCheckBox.is_selected() != True:
            try:
                newCheckBox.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", newCheckBox)
                except:
                    newCheckBox.send_keys(Keys.SPACE)
    porabaOBJAVI = driver.find_element_by_name("porabaOBJAVI")
    if porabaOBJAVI.is_selected():
        porabaOBJAVI.click()
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
     WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[3]/a/strong"))).click()
    except:
        print("")
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
    WebDriverWait(driver, 10).until(ec.alert_is_present(),"")
    time.sleep(5)
    driver.switch_to.alert.accept()
    time.sleep(2)


    print("=> prvotni oglas je izbrisan ")


def zapriBrowser():
    global imenaSlik
    imenaSlik = []


def pokaziPopup():
    tk.messagebox.showinfo("Opozorilo", "Program bo izbrisal oglas/e med procesom ne uporabljajte miške ali \n tipkovnice  in počakajte da se brskalnik samostojno vgasne.", )


def main():

    pause = int(pauseEntry.get())


    urlji= []
    root.withdraw()
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    print("=> vsi gonilniki uspešno pridobljeni")

    driver.get("https://www.avto.net/_2016mojavtonet/")
    driver.maximize_window()
    global originalOglasWindow
    originalOglasWindow = driver.window_handles[0]
    login(email, geslo)
    driver.get("https://www.avto.net/_2016mojavtonet/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000001000&EQ7=1110100122&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=11084&prikazkategorije=0&kategorija=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran=1&subSORT=3&subTIPSORT=ASC")
    results = driver.find_elements_by_class_name("ResultsAd")
    for result in results :
        try:
            result.find_element_by_class_name("ResultsAdPriceRegular")
            urlji.append(result.find_element_by_class_name("Adlink").get_attribute("href"))
        except:
            print("Avto je že prodan")

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
        driver.switch_to.window(driver.window_handles[0])
        print("Obnovil sem toliko oglasov:"+str(urlji.index(url)+1))
        time.sleep(pause*60)




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

button1 = tk.Button(text='Izbriši in ponovno ustvari vse oglase', command=lambda: [main()], bg='white', fg='black',font=('helvetica', 10, 'bold'))
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

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("avtonetdata/creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("avtonetbot dostop").sheet1  # Open the spreadhseet

try:
    emailRow = sheet.find(email).row
    placanoCell = sheet.cell(emailRow,2).value.strip()
    if placanoCell == "NE":
        print("NISTE NAROČENI NA PROGRAM!")
        print("ZA NAKUP PROGRAMA PIŠITE NA gal.jeza@protonmail.com")
        print("ČE STE NAROČENI NA PROGRAM IN VSEENO VIDITE TO SPOROČILO ME KONTAKTIRAJTE")
    else:
        root.mainloop()
except:
    print("NISTE NAROČENI NA PROGRAM!")
    print("ZA NAKUP PROGRAMA PIŠITE NA gal.jeza@protonmail.com")
    print("ČE STE NAROČENI NA PROGRAM IN VSEENO VIDITE TO SPOROČILO ME KONTAKTIRAJTE")
    time.sleep(30)
