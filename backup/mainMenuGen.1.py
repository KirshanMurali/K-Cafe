import pickle
from Database import UDB
def loadStaffs():
    Users=[
        {'username':'admin','password':'kidocode', 'email':'email', 'userimage':'/static/theCreators.jpg'},
        {'username':'maysam','password':'kidocode', 'email':'email', 'userimage':'/static/maysam.jpg'},
        {'username':'arsham','password':'kidocode', 'email':'email', 'userimage':'/static/arsham.jpg'},
        {'username':'kirshan','password':'kidocode', 'email':'email', 'userimage':'/static/kirshan.jpg'},
        {'username':'mojgan','password':'kidocode', 'email':'email', 'userimage':'/static/mojgan.jpg'},
        {'username':'hannah','password':'kidocode', 'email':'email', 'userimage':'/static/hannah.jpg'},
        {'username':'unclecode','password':'kidocode', 'email':'email', 'userimage':'/static/unclecode.jpg'},
        {'username':'iniobong','password':'kidocode', 'email':'email', 'userimage':'/static/iniobong.jpg'},
        {'username':'hada','password':'kidocode', 'email':'email', 'userimage':'/static/hada.jpg'},
        {'username':'jack','password':'kidocode', 'email':'email', 'userimage':'/static/jack.jpg'},
        {'username':'diyana','password':'kidocode', 'email':'email', 'userimage':'/static/diyana.jpg'},
        {'username':'dayana','password':'kidocode', 'email':'email', 'userimage':'/static/dayana.jpg'},
        {'username':'ohkeehau','password':'kidocode', 'email':'email', 'userimage':'/static/ohkeehau.jpg'},
        {'username':'sinjunlou','password':'kidocode', 'email':'email', 'userimage':'/static/sinjunlou.jpg'},
        {'username':'son','password':'kidocode', 'email':'email', 'userimage':'/static/son.jpg'},
        {'username':'thivyadarshini','password':'kidocode', 'email':'email', 'userimage':'/static/thivyadarshini.jpg'},
        {'username':'paulinelow','password':'kidocode', 'email':'email', 'userimage':'/static/paulinelow.jpg'},
        {'username':'pavitrasheilian','password':'kidocode', 'email':'email', 'userimage':'/static/pavitrasheilian.jpg'},
        {'username':'tabihta','password':'kidocode', 'email':'email', 'userimage':'/static/tabihta.jpg'},
        {'username':'mohammed','password':'kidocode', 'email':'email', 'userimage':'/static/mohammed.jpg'},
        {'username':'vee','password':'kidocode', 'email':'email', 'userimage':'/static/vee.jpg'},
        {'username':'yvonne','password':'kidocode', 'email':'email', 'userimage':'/static/yvonne.jpg'},
        {'username':'arash','password':'kidocode', 'email':'email', 'userimage':'/static/arash.jpg'},
        {'username':'ash','password':'kidocode', 'email':'email', 'userimage':'/static/ash.jpg'},
        {'username':'chojianwei','password':'kidocode', 'email':'email', 'userimage':'/static/chojianwei.jpg'},
        {'username':'rocill','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'anne','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'ray','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'zul','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'sherrie','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'shema','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'adrian','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'ani','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'jacky','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'erick','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'muaz','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'idris','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        {'username':'ken','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
    ]
    
    for new in Users:
        newUser=UDB.User(new)
        UDB.add(newUser)
        
    
    
    
def loadFood():
    f = open('mainMenu.pkl', 'wb')
    mainMenu={
        'VegetablePasta':{'foodname':'VegetablePasta','foodimage':'/static/VegetablePasta.jpg','price':17},
        'VegetableKebab':{'foodname':'VegetableKebab','foodimage':'/static/VegetableKebab.jpg','price':17},
        'Tahchin':{'foodname':'Tahchin','foodimage':'/static/Tahchin.jpg','price':17},
        'Kotlet':{'foodname':'Kotlet','foodimage':'/static/Kotlet.jpg','price':15},
        'KhashKhashKebab':{'foodname':'KhashKhashKebab','foodimage':'/static/KhashKhashKebab.jpg','price':17},
        'KebabKoobide':{'foodname':'KebabKoobide','foodimage':'/static/KebabKoobide.jpg','price':17},
        'JoojeKebab':{'foodname':'JoojeKebab','foodimage':'/static/JoojeKebab.jpg','price':17},
        'HotDog':{'foodname':'HotDog','foodimage':'/static/HotDog.jpg','price':15},
        'GhormesabziStew':{'foodname':'GhormesabziStew','foodimage':'/static/GhormesabziStew.jpg','price':15},
        'GheymeStew':{'foodname':'GheymeStew','foodimage':'/static/GheymeStew.jpg','price':15},
        'GheymeAndEggPlantStew':{'foodname':'GheymeAndEggPlantStew','foodimage':'/static/GheymeAndEggPlantStew.jpg','price':15},
        'CheeseBurger':{'foodname':'CheeseBurger','foodimage':'/static/CheeseBurger.jpg','price':15},
        'CeleryStew':{'foodname':'CeleryStew','foodimage':'/static/CeleryStew.jpg','price':15},
        'BreastChickenLari':{'foodname':'BreastChickenLari','foodimage':'/static/BreastChickenLari.jpg','price':17},
        'BeefTongue':{'foodname':'BeefTongue','foodimage':'/static/BeefTongue.jpg','price':15},
        'BeefTomatoPasta':{'foodname':'BeefTomatoPasta','foodimage':'/static/BeefTomatoPasta.jpg','price':17},
        'LobiyaPolo':{'foodname':'LobiyaPolo','foodimage':'/static/LobiyaPolo.jpg','price':17},
        'BarberryRiceChickenStew':{'foodname':'BarberryRiceChickenStew','foodimage':'/static/BarberryRiceChickenStew.jpg','price':17},
        'JumboCheeseChickenHotDog':{'foodname':'JumboCheeseChickenHotDog','foodimage':'/static/JumboCheeseChickenHotDog.jpg','price':10.50},
        'PepperoniBeefPizza':{'foodname':'PepperoniBeefPizza','foodimage':'/static/BeefPepperoniPizza.jpg','price':13.50},
        'ChickenHawaiianPizza':{'foodname':'ChickenHawaiianPizza','foodimage':'/static/HawianChickenPizza.jpg','price':13.50},
        'AglioOlioMushroomSpaghetti':{'foodname':'AglioOlioMushroomSpaghetti','foodimage':'/static/AglioOlioMushroomSpaghetti.jpg','price':16.50},
        'CheesyMushroomChickenBakedRice':{'foodname':'CheesyMushroomChickenBakedRice','foodimage':'/static/cmcbr.jpg','price':''},
        'BeefCarbonaraSpaghetti':{'foodname':'BeefCarbonaraSpaghetti','foodimage':'/static/beefCarbonaraSpaghetti.jpg','price':18.50},
        'BologneseChickenSpaghetti':{'foodname':'BologneseChickenSpaghetti','foodimage':'/static/BologneseChickenSpaghetti.jpg','price':16.50},
        'PadThaiSpicy':{'foodname':'PadThaiSpicy','foodimage':'/static/padThai.jpg','price':''},
        'ChickenFriedRice':{'foodname':'ChickenFriedRice','foodimage':'/static/chickenFriedRice.jpg','price':''},
        'Stir-FriedChickenBasilLeafSpicy':{'foodname':'Stir-FriedChickenBasilLeafSpicy','foodimage':'/static/Stir-FriedChickenBasilLeaf(Spicy).jpg','price':11},
        'TomYamBihun':{'foodname':'TomYamBihun','foodimage':'/static/tomyamBihun.jpg','price':11},
        'Bobcat(Beef)':{'foodname':'Bobcat(Beef)','foodimage':'/static/bobcatBeef.JPG','price':15.90},
        'Bobcat(Chicken)':{'foodname':'Bobcat(Chicken)','foodimage':'/static/BobcatChicken.jpg','price':15.90},
        'Tornado(Chicken)':{'foodname':'Tornado(Chicken)','foodimage':'/static/tornado.jpg','price':16.90},
        'Bash(Beef)':{'foodname':'Bash(Beef)','foodimage':'/static/bashbeef.jpg','price':18.90}
    }
    pickle.dump(mainMenu,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    
    f = open('sessionStatus.pkl', 'wb')
    sessionStatus={'sessionStatus':'close'}
    pickle.dump(sessionStatus,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    
    return 'done!'
loadFood()
loadStaffs()