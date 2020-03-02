# -*-coding:utf-8 -*-

import discord as d
import requests as req
import map as m
import json

TOKEN = "NjMxNTY4MDkyOTQ1OTczMjU4.Xlwcvw.Ef7iksQqcpqU0m-ei3TEDx-tMGc"

URL = "https://api.myjson.com/bins/ur3rm"

Default_Prefix = "hmap"

Dataset = ["bliiury","jensensuk","katnova",
            "keraketh","petbel","mupenium",
            "nimelerty","dymnova","rolria",
            "pexelerty","thuerty","pentenubula",
            "zionueva","japubula","cinroid",
            "trisikon","jelodia","asuvania",
            "parerth","elodreus","galuslise",
            "blokenutea","zynellax""nomelran",
            "rotenubel","vicran","thorovania",
            "dinkon","noiorind","pezigua",
            "junaliv","limioid","nudonova",
            "catiria","jungus","clausnova",
            "noitea","galea","qurind",
            "charenuroid","kapdam","reslore",
            "acisennus","dinelzar","rivlis",
            "mulivania","elodreus","xanuslia",
            "jesjor","xamrad","thonvania",
            "jesenudam","nimusran","rotusgua",
            "metagua","japlax","blisia",
            "icrahiri","purilia","cheapra",
            "kicrerus","thacragua","suveron",
            "triugawa","chenanov","robraclite",
            "cistruenus","linzone","xistreshan",
            "iulea","kuanides","zilanus","brupuvis"]

Colors = {"darkblue" : [15,5,107]}

Client = d.Client()

@Client.event

async def on_ready () :

    req.put(URL, json = {"travelers" : {}, "systems" : {}})
                
    await Client.change_presence(status = d.Status.online, activity = d.Activity(type = d.ActivityType.watching, name = "the galaxy"))

    Client.Infos = await Client.application_info()

    Client.Owner = Client.get_user(Client.Infos.owner.id)

    print("READY")

@Client.event

async def on_message (message) :

    if message.author == Client.user :

        return

    Msg = message.content

    Response = req.get(URL)
    
    Database = json.loads(Response.text)

    MAP = m.Map(Database, Dataset)

    PLAYERS = m.Players(Database)
    PLAYERS.set_Player(str(message.author.id))

    SHIPS = m.Ships(Database)
    SHIPS.set_Player(str(message.author.id))

    if Msg.startswith(Default_Prefix) :

        Command = Msg[len(Default_Prefix)+1:]

        if Command == "begin" :

            if str(message.author.id) not in Database["travelers"] :

                PLAYERS.create_Player(str(message.author.id), str(message.author))
                SHIPS.create_Default()

                PLAYERS.add_Achievement("First Step")
                PLAYERS.add_Money(2000)

                System_Name = str(MAP.create_System(str(message.author.id), begin = True))
                Informations = MAP.get_System(System_Name)

                Infos = ""
                Infos += "\nHub : " + str(Informations["hub"])
                Infos += "\nGas station : " + str(Informations["station"])
                Infos += "\nEconomy : " + str(Informations["economy"])
                Infos += "\nPlanets : " + str(Informations["planets"])
                Infos += "\nSystem sizes : " + str(Informations["sizes"])
                Infos += "\nLocation : " + str(Informations["coords"])
                
                Description = "**We are all lost stars trying to shine in the dark...**\n\nI just woke up in a system named " + System_Name + ",\nAll I can remember is my name and a message repeating in my com saying : ```reach th... krch.kr cente.krchhh...```"

                Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                    title = ":book: Achievement unlock : First step :moneybag: +2000",
                                    description = Description)

                Embed.add_field(name = "**Informations about the system :**", value = Infos)
                Embed.set_thumbnail(url = "https://www.muyinteresante.com.mx/wp-content/uploads/2018/05/httpstved-prod.adobecqms.netcontentdameditorialTelevisamexicomuyinteresantemxespacio1406olor-en-el-centro-de-la-galaxia-1080x764.imgo_.jpg")

            else :

                Description = "You can only use this command once to create your character"
                
                Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                    title = ":no_entry: You can't use this command",
                                    description = Description)
                
        if str(message.author.id) in Database["travelers"] :
            
            if Command == "mystats" :

                if "Know yourself" not in PLAYERS.get_Achievements() :

                    PLAYERS.add_Achievement("Know yourself")
                    PLAYERS.add_Money(2000)

                    Description = "**Knowing yourself is the beginning of all wisdom.**\n\nI just remember that I have personal a personal recorder, I'm going to check it... ```RECORDER INITIALIZED, BEGINNING DATA EXTRACTION```"

                    Title = ":book: Achievement unlock : Know yourself :moneybag: +2000"

                    Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                        title = Title,
                                        description = Description)

                else :

                    Title = ":bar_chart: Player statistics :"

                    Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                        title = Title)

                Embed.add_field(name = "Apparition :", value = PLAYERS.apparition())

                Embed.add_field(name = "Location :", value = PLAYERS.current_Location())

                Embed.add_field(name = "Units travelled :", value = PLAYERS.get_Units())

                Embed.add_field(name = "Systems dicovered :", value = str(len(PLAYERS.get_Discover())))

                Embed.add_field(name = "Achievements :", value = str(len(PLAYERS.get_Achievements())))
                
                Embed.add_field(name = "Money :", value = str(PLAYERS.money()))

                Ship = PLAYERS.current_Ship()["name"]

                Ship = Ship[0].upper() + Ship[1:]

                Embed.add_field(name = "Current ship :", value = Ship)

                Embed.add_field(name = "Ships in depot :", value = str(len(PLAYERS.get_Ships())))
                
                Embed.set_thumbnail(url = Client.Infos.icon_url)

            elif Command == "ship" :

                Ship = PLAYERS.current_Ship()
                
                Catalog = SHIPS.get_Catalog()

                for specs in Catalog :

                    if specs["name"] == Ship["name"] :

                        Max_Fuel = specs["fuel"]

                        break

                if "My baby" not in PLAYERS.get_Achievements() :

                    PLAYERS.add_Achievement("My baby")
                    PLAYERS.add_Money(2000)

                    Description = "**Aviation is proof that given, the will, we have the capacity to achieve the impossible.**\n\nOH ! I think I found an other really cool function ! ```SHIP SPECIFICATIONS ANALYZED```"

                    Title = ":book: Achievement unlock : My baby :moneybag: +2000"

                    Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                        title = Title,
                                        description = Description)

                else :

                    Title = ":bar_chart: Ship statistics :"

                    Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                        title = Title)

                Name = Ship["name"][0].upper() + Ship["name"][1:]

                Embed.add_field(name = "Shipname :", value = Name)

                Embed.add_field(name = "Units travelled :", value = str(Ship["units"]))

                Embed.add_field(name = "Number of systems dicovered :", value = str(Ship["systems_discovered"]))

                Embed.add_field(name = "Current fuel :", value = str(Ship["fuel"]))

                Embed.add_field(name = "Max fuel :", value = str(Max_Fuel))

                Embed.add_field(name = "Range :", value = str(Ship["range"]))

                Embed.add_field(name = "Damage percent :", value = str(Ship["damaged"]) + "%")

            elif Command == "myships" :

                Ships = ""

                Range = ""

                Fuel = ""

                for ship in PLAYERS.get_Ships() :

                    Ships += "\n" + ship[0].upper() + ship[1:]

                    Infos = PLAYERS.ship_Infos(ship)

                    Range += "\n" + str(Infos["range"])

                    Fuel += "\n" + str(Infos["fuel"])

                Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                    title = ":briefcase: Ships in depot :")

                Embed.add_field(name = "Ship :", value = Ships, inline = True)

                Embed.add_field(name = "Range :", value = Range, inline = True)

                Embed.add_field(name = "Fuel :", value = Fuel, inline = True)

            elif Command.startswith("buyship") :

                Shipname = Command[8:].lower()

                Result = SHIPS.buy_Ship(Shipname)

                if Result == True :

                    Description = "Congratulations, you just bought the " + Command[8:] + " model"

                elif Result == False :

                    Description = "Sorry but the model name you want don't exist"

                else :

                    Description = "Sorry but you don't have enought money to pay this model, you need " + str(Result) + " $ more."

                Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                    title = ":department_store: Transaction result :",
                                    description = Description)            

            elif Command == "catalog" :

                Catalog = SHIPS.get_Catalog()

                Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                    title = ":rocket: Ships catalog :")

                for specs in Catalog :

                    Name = specs["name"][0].upper() + specs["name"][1:]

                    Value = "Range : " + str(specs["range"]) + "\n" + "Fuel : " + str(specs["fuel"]) + "\n" + "Price : " + str(specs["price"])

                    Embed.add_field(name = Name, value = Value)

            elif Command == "systems" :

                Knowed_Systems = MAP.list_Systems()

                Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                    title = ":map: Systems discovered :")

                Embed.add_field(name = "Number of systems discovered :", value = len(Knowed_Systems))

                Names = ""

                for system in Knowed_Systems :

                    Names += "\n" + system

                Embed.add_field(name = "Systems discovered :", value = Names)

            elif Command.startswith("travel") :

                Travel = nonglobal Command[7:]

                Travel = eval(Travel)

                print(Travel)

                print(type(Travel))

                if type(Travel) == list or type(Travel) == tuple :

                    Result = SHIPS.travel_To(Travel)

                elif type(Travel) == int or type(Travel) == float :

                    Result = SHIPS.travel_To([Travel,Travel])

                else :

                    print("Planet name")
        else :

            Description = "To use the commands you need to begin the adventure first, to begin the adventure type :\n```" + Default_Prefix + " begin```"

            Embed = d.Embed(color = d.Color.from_rgb(Colors["darkblue"][0],Colors["darkblue"][1],Colors["darkblue"][2]),
                                title = ":no_entry: Access refused :",
                                description = Description)
            

    await message.channel.send(embed = Embed)

    req.put(URL, json = Database)

Client.run(TOKEN, bot = True)
