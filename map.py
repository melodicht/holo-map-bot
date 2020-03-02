import random as rd

class Map : #Galactical map class

    def __init__ (self, dataset, entries) : #Initialisation of the galactic map

        """A creator and manager for galactical map"""

        self.dataset = dataset #Passing the dataset to global

        self.entries = self.create_Entries(entries) #Creating entries for names

    def generate_Name (self) :

        Num = ["II","III","IV","V",
               "VI","VII","VIII","IX"]

        Planet_Type = ["Minor","Minus","Major","Alpha","Beta","Delta"]

        Max_Length = rd.randint(5,10)

        Name = ""

        Last = ""

        while len(Name) < Max_Length :

            Part = rd.choice(self.entries)

            if Last != "" :

                if len(Last) < 1 :

                    if Last != Part :

                        if Last[1] != Part[0] :

                            Name += Part

                else :

                    if Last != Part :

                        Name += Part

            Last = Part

        Name = Name[0].upper() + Name[1:]

        Bool = [True, False]

        if rd.choice(Bool) == True :

            Choice = rd.choice(Bool)

            if Choice == True :

                Name += " " + rd.choice(Num)

            else :

                Type = rd.choice(Planet_Type)

                Name += " " + Type

                if Choice != True :

                    if rd.choice(Bool) == True :

                        Name += " " + rd.choice(Num)

        return Name

    def create_System (self, playerid, coords = None, begin = False) :

        System_Name = self.generate_Name()

        if begin == True :

            Coords = rd.randint(70000000,99999999), rd.randint(70000000,99999999)

            System_Sizes = rd.randint(30000,49999), rd.randint(10000,49999)

            Planets_Number = rd.randint(6,9)

            Bool_Station = True

            Bool_Hub = True

            Economy = rd.choice(["stable","rich"])

            self.dataset["travelers"][playerid]["apparition"] = System_Name

        else :

            Coords = coords

            System_Sizes = rd.randint(9999,29999), rd.randint(9999,29999)

            Probability = rd.randint(0,100)

            if Probability >= 92 :

                Planets_Number = rd.randint(5,8)

                Economy = "rich"

                Bool_Station = True

                Bool_Hub = True

            elif Probability >= 70 :

                Planets_Number = rd.randint(4,7)

                Economy = "stable"

                Probability = rd.randint(0,100)

                if Probability >= 60 :

                    Bool_Station = True

                else :

                    Bool_Station = False

                Probability = rd.randint(0,100)

                if Probability >= 80 :

                    Bool_Hub = True

                else :

                    Bool_Hub = False
                
            elif Probability >= 10 :

                Planets_Number = rd.randint(2,4)

                Economy = "poor"

                Probability = rd.randint(0,100)

                if Probability >= 80 :

                    Bool_Station = True

                else :

                    Bool_Station = False

                Bool_Hub = False

            else :

                Planets_Number = rd.randint(0,2)

                Economy = "inexistant"

                Bool_Station = False

                Bool_Hub = False

        self.dataset["systems"][System_Name] = {"coords" : [Coords[0],Coords[1]],"sizes" : System_Sizes,"explored_by" : playerid,"economy" : Economy, "planets" : Planets_Number,"station" : Bool_Station, "hub" : Bool_Hub}  

        self.dataset["travelers"][playerid]["discovered"].append(System_Name)

        self.dataset["travelers"][playerid]["current_location"] = [rd.randint(1000,System_Sizes[0]), rd.randint(1000, System_Sizes[1])]

        self.dataset["travelers"][playerid]["current_ship"]["systems_discovered"] += 1
        
        return System_Name
    
    def get_System (self, name) : #Select a system by name

        """Get all the informations about a given system"""

        for system in self.dataset["systems"] : #Iterate over all the systems in the dataset

            if system == name : #If the current system is the system we want

                return self.dataset["systems"][system] #Return the informations about the system

        return False #Return False if no system exist for the given name

    def at_Coords (self, coords) : #Verify if a system exist at the given coords

        """A verifier for existing system at the given coords"""

        for system in self.dataset["systems"] : #Iterate over all existing systems in the dataset

            System_Coords = self.dataset["systems"][system]["coords"] #Get the coords of the system

            System_Sizes = self.dataset["systems"][system]["sizes"] #Get the sizes of the system

            if coords[0] in range (-System_Coords[0] - System_Sizes[0], System_Coords[0] + System_Sizes[0]) and coords[1] in range (-System_Coords[1] - System_Sizes[1], System_Coords[1] + System_Sizes[1]) : #If the given coords are inside the coords of the system

                return system #Return the name of the system

        return False #Return None if no system detected

    def list_Systems (self) : #List all the systems in the dataset

        """List all the systems present in the dataset"""

        Systems = [] #List to contain all the systems name

        for system in self.dataset["systems"] : #Iterate over all the systems

            Systems.append(system) #Add the name of the system to the list

        return Systems #Return all the systems name

    def create_Entries (self, bag) : #Generate the bag of words for the systems name

        """Generate part of name for the systems"""

        Vowels = 'aeiouy' #Vowels to detect in a word

        List = [] #List containing all the entries

        for word in bag :
        
            Count = 0
            
            if word[0] in Vowels :

                List.append(word[0])
                
                Count += 1

            else :

                Sequence = word[0]
                
            for index in range(1, len(word)):

                Sequence += word[index]
                
                if word[index] in Vowels and word[index - 1] not in Vowels :
                    
                    Count += 1

                    List.append(Sequence)

                    Sequence = ""
                    
            if word.endswith('e'):

                List.append(word[len(word)-1])
                
                Count -= 1
                
            if word.endswith('le') and len(word) > 2 and word[-3] not in Vowels :

                List[len(List)-1] = List[len(List)-1] + word[len(word)-1]
                
                Count += 1
                
            if Count == 0:

                List[len(List)-1] = List[len(List)-1] + word[len(word)-1]
                
                Count += 1
            
        return List

class Players :

    Default_Traveler = {"name" : None,"discovered" : [],"units" : 0,"current_ship" : None, "ships_owned" : [],"money" : 1000,"apparition" : [],"current_location" : [],"achievements" : []}

    def __init__ (self, dataset) :

        self.dataset = dataset

    def set_Player (self, unique_id) :

        self.unique_id = unique_id

    def get_Player (self, player_id) :

        for unique_id in self.dataset["travelers"] :

            if unique_id == player_id :

                return self.dataset["travelers"][unique_id]

        return False

    def create_Player (self, unique_id, playername) :

        self.dataset["travelers"][unique_id] = self.Default_Traveler

        self.dataset["travelers"][unique_id]["name"] = playername

    def add_Achievement (self, name) :

        self.dataset["travelers"][self.unique_id]["achievements"].append(name)

    def get_Achievements (self) :

        return self.dataset["travelers"][self.unique_id]["achievements"]

    def current_Ship (self) :

        return self.dataset["travelers"][self.unique_id]["current_ship"]

    def select_Ship (self, shipname) :

        for specs in self.dataset["travelers"][self.unique_id]["ships_owned"] :

            if specs["name"] == shipname :

                self.dataset["travelers"][self.unique_id]["current_ship"] = specs

                return True
            
        return False

    def ship_Infos (self, shipname) :

        for specs in self.dataset["travelers"][self.unique_id]["ships_owned"] :

            if specs["name"] == shipname :

                return specs

        return False

    def get_Ships (self) :

        List = []

        for specs in self.dataset["travelers"][self.unique_id]["ships_owned"] :

            List.append(specs["name"])

        return List

    def current_Location (self) :

        return self.dataset["travelers"][self.unique_id]["current_location"]

    def money (self) :

        return self.dataset["travelers"][self.unique_id]["money"]

    def add_Money (self, amount) :

        self.dataset["travelers"][self.unique_id]["money"] = self.dataset["travelers"][self.unique_id]["money"] + amount

    def remove_Money (self, amount) :

        self.dataset["travelers"][self.unique_id]["money"] = self.dataset["travelers"][self.unique_id]["money"] - amount

    def add_Units (self, amount) :

        self.dataset["travelers"][self.unique_id]["units"] = self.dataset["travelers"][self.unique_id]["units"] + amount

    def get_Units (self) :

        return self.dataset["travelers"][self.unique_id]["units"]

    def apparition (self) :

        return self.dataset["travelers"][self.unique_id]["apparition"]

    def get_Discover (self) :

        return self.dataset["travelers"][self.unique_id]["discovered"]

class Ships :

    Default_Category = {"mustang" : {"name" : "mustang","units" : 0,"fuel" : 2000,"damaged" : 0,"range" : 500,"price" : 100000,"systems_discovered" : 0},
                        "falcon" : {"name" : "falcon","units" : 0,"fuel" : 2000,"damaged" : 0,"range" : 500, "price" : 300000,"systems_discovered" : 0}
                        }

    Category = {"mustang" : {"name" : "mustang","units" : 0,"fuel" : 2000,"damaged" : 0,"range" : 500,"price" : 100000,"systems_discovered" : 0},
                "falcon" : {"name" : "falcon","units" : 0,"fuel" : 2000,"damaged" : 0,"range" : 500, "price" : 300000,"systems_discovered" : 0}
                }

    def __init__ (self, dataset) :

        self.dataset = dataset

    def set_Player (self, unique_id) :

        self.unique_id = unique_id

    def create_Default (self) :

        Default_Ship = self.Default_Category["mustang"]

        self.dataset["travelers"][self.unique_id]["current_ship"] = Default_Ship

        self.dataset["travelers"][self.unique_id]["ships_owned"].append(Default_Ship)

    def buy_Ship (self, shipname) :

        Ship = None

        for ship in self.Default_Category :

            print(ship)

            if ship == shipname :

                Ship = self.Default_Category[ship]

                break

        if Ship == None :

            return False

        print(self.dataset["travelers"])

        Difference = self.dataset["travelers"][self.unique_id]["money"] - Ship["price"]

        if Difference < 0 :

            return abs(Difference)

        else :

            self.dataset["travelers"][self.unique_id]["ships_owned"].append(Ship)

            return True

    def get_Catalog (self) :

        List = []

        for ship in self.Default_Category :

            List.append(self.Default_Category[ship])

        return List
    
    def remove_Fuel (self, amount) :

        New = abs(amount - self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"])

        self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"] = New

        for specs in self.dataset["travelers"][self.unique_id]["ships_owned"] :

            if specs["name"] == self.dataset["travelers"][self.unique_id]["current_ship"]["name"] :

                specs["fuel"] = New

                return

    def resupply_Fuel (self) :

        Default_Fuel = self.Category[self.dataset["travelers"][self.unique_id]["current_ship"]["name"]]["fuel"]

        self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"] = Default_Fuel

        for specs in self.dataset["travelers"][self.unique_id]["ships_owned"] :

            if specs["name"] == self.dataset["travelers"][self.unique_id]["current_ship"]["name"] :

                specs["fuel"] = Default_Fuel

                return
    def travel_To (self, coords) :

        if self.dataset["travelers"][self.unique_id]["current_ship"]["range"] >= coords[0] or self.dataset["travelers"][self.unique_id]["current_ship"]["range"] >= coords[1] :

            Difference_X = abs(coords[0] - self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"])

            Difference_Y = abs(coords[1] - self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"])

            if self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"] >= coords[0] or self.dataset["travelers"][self.unique_id]["current_ship"]["fuel"] >= coords[1] :

                if Difference_X == 0 or Difference_Y == 0 :

                    return False

                else :

                    if coords[0] >= coords[1] :

                        self.remove_Fuel(coords[0])

                    else :

                        self.remove_Fuel(coords[1])

                    return True
                
        else :

            return None

##########################################METHODS####################################################################
#Map :
#Map.create_System([coords[0], coords[1]], playerid, begin)
#Map.get_System(name) Return the system name if it exist or False if no system exist with the given name
#Map.at_Coords([coords[0], coords[1]) Return the system name if one is located in the given coords or return False if there is no existing system at the given coords
#Map.list_Systems()

#Players :
#Players.set_Player(id)
#Players.create_Player(id, name)
#Players.get_Player(id)
#Players.current_Ship()
#Players.select_Ship(name)
#Players.ship_Infos(name)
#Players.get_Ships()
#Players.current_Location()
#Players.money()
#Players.add_Money(amount)
#Players.remove_Money(amount)
#Players.add_Units(amount)
#Players.get_Units()
#Players.apparition()
#Players.get_Discover()

#Ships :
#Ships.set_Player(id)
#Ships.create_Default()
#Ships.buy_Ship()
#Ships.get_Catalog()
#Ships.remove_Fuel(amount)
#Ships.resupply_Fuel(amount)
#Ships.travel_To([coords[0], coords[1])
            

