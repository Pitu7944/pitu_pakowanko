import eel, sys, os
import random
import json, shutil
import logging, subprocess
from xml.dom import minidom
#main color scheme : https://coolors.co/03071e-370617-6a040f-9d0208-d00000-dc2f02-e85d04-f48c06-faa307-ffba08

logging.basicConfig(level=logging.DEBUG)

resource_data ="""resource_manifest_version '77731fab-63ca-442c-a67b-abc70f28dfa5'
description "Pitu_Pakowanko_v3 CarPack"
files {
    'data/**/vehicles.meta',
    'data/**/carvariations.meta',
    'data/**/carcols.meta',
    'data/**/handling.meta',
}

data_file 'HANDLING_FILE' 'data/**/handling.meta'
data_file 'VEHICLE_METADATA_FILE' 'data/**/vehicles.meta'
data_file 'CARCOLS_FILE' 'data/**/carcols.meta'
data_file 'VEHICLE_VARIATION_FILE' 'data/**/carvariations.meta'
"""

watermark = """--[[
 ____  _ _        _____ ___  _  _   _  _     _  _  ____ _____ _ _ 
|  _ \(_) |_ _   |___  / _ \| || | | || |  _| || ||___ \___  / / |
| |_) | | __| | | | / / (_) | || |_| || |_|_  ..  _|__) | / /| | |
|  __/| | |_| |_| |/ / \__, |__   _|__   _|_      _/ __/ / / | | |
|_|   |_|\__|\__,_/_/    /_/   |_|    |_|   |_||_||_____/_/  |_|_|
]]
"""

resource_data += watermark


@eel.expose
def show_log(text):
    eel.addToLog(text)
    print(text)



class Pakowanko:
    def __init__(self):
        self.data = {}
        if os.path.exists("./pakowanko"):
            shutil.rmtree('./pakowanko')
            os.mkdir('./pakowanko')
        else:
            os.mkdir('./pakowanko')

        if os.path.exists("./pakowanko/output"):
            shutil.rmtree('./pakowanko/output')
            os.mkdir('./pakowanko/output')
        else:
            os.mkdir('./pakowanko/output')

        if os.path.exists("./pakowanko/input"):
            shutil.rmtree('./pakowanko/input')
            os.mkdir('./pakowanko/input')
        else:
            os.mkdir('./pakowanko/input')

        if os.path.exists("./pakowanko/pack_to_modify"):
            shutil.rmtree('./pakowanko/pack_to_modify')
            os.mkdir('./pakowanko/pack_to_modify')
        else:
            os.mkdir('./pakowanko/pack_to_modify')

        if os.path.exists("./pakowanko/modify_input"):
            shutil.rmtree('./pakowanko/modify_input')
            os.mkdir('./pakowanko/modify_input')
        else:
            os.mkdir('./pakowanko/modify_input')        
        
        if os.path.exists("./pakowanko/output/data"):
            shutil.rmtree('./pakowanko/output/data')
            os.mkdir('./pakowanko/output/data')
        else:
            os.mkdir('./pakowanko/output/data')

    def get_input_content(self):
        files = []
        if os.path.exists('./pakowanko/input'):
            files = os.listdir('./pakowanko/input')
            self.data['carlist'] = files
            for car in files:
                self.data[car] = {
                    "model": car,
                    "spawnname": self.get_car_spawn_name(car),
                    "files": {
                        "handling": [],
                        "stream": []
                    }
                }
                logging.info(f"Processing {car}")
                show_log(f"Processing {car}")
                car_stream = os.listdir(f"./pakowanko/input/{car}/stream")
                handling_files = self.get_handling_files(car)
                for model_data_file in car_stream:
                    self.data[car]['files']['stream'].append(model_data_file)
                    show_log(f"Adding file {model_data_file}")
                    logging.debug(f"Adding file {model_data_file}")
                for handling_data_file in handling_files:
                    self.data[car]['files']['handling'].append(handling_data_file)
                    show_log(f"Adding file {handling_data_file}")
                    logging.debug(f"Adding file {handling_data_file}")
        logging.debug(self.data)
        return files

    def get_handling_files(self, car):
        car_dir = os.listdir(f"./pakowanko/input/{car}/")
        handling_files = []
        for handling_file in car_dir:
            if handling_file.endswith('.meta'):
                handling_files.append(handling_file)
        return handling_files

    def process_handling_files(self):
        for car_name in self.data['carlist']:
            car_files = self.data[car_name]['files']['handling']
            if os.path.exists(f"./pakowanko/output/data/{car_name}"):
                shutil.rmtree(f"./pakowanko/output/data/{car_name}")
                show_log(f"Removing existing folder for handling data of {car_name}")
                os.mkdir(f"./pakowanko/output/data/{car_name}")
                show_log(f"Creating folder for handling data of {car_name}")
            else:
                os.mkdir(f"./pakowanko/output/data/{car_name}")
                show_log(f"Creating folder for handling data of {car_name}")
            for handling_file in car_files:
                shutil.copy(f"./pakowanko/input/{car_name}/{handling_file}", f"./pakowanko/output/data/{car_name}/{handling_file}")
        return True

    def process_stream_files(self):
        if os.path.exists(f"./pakowanko/output/stream"):
            shutil.rmtree(f"./pakowanko/output/stream")
            os.mkdir(f"./pakowanko/output/stream")
        else:
            os.mkdir(f"./pakowanko/output/stream")
        for car_name in self.data['carlist']:
            car_files = self.data[car_name]['files']['stream']
            if os.path.exists(f"./pakowanko/output/stream/{car_name}"):
                show_log(f"Removing existing folder for stream textures of {car_name}")
                shutil.rmtree(f"./pakowanko/output/stream/{car_name}")
                show_log(f"Creating folder for stream textures of {car_name}")
                os.mkdir(f"./pakowanko/output/stream/{car_name}")
            else:
                os.mkdir(f"./pakowanko/output/stream/{car_name}")
            for stream_file in car_files:
                shutil.copy(f"./pakowanko/input/{car_name}/stream/{stream_file}", f"./pakowanko/output/stream/{car_name}/{stream_file}")
                show_log(f"Copying {car_name}/{stream_file} to stream textures of {car_name}")
        return True

    def init_resource_file(self):
        with open('./pakowanko/output/__resource.lua', 'w') as f:
            f.write(resource_data)
        show_log("Initializing __resource.lua file for pack")
        return True
    
    def get_car_spawn_name(self, car):
        handling_data = minidom.parse(f'./pakowanko/input/{car}/handling.meta')
        handling_elements = handling_data.getElementsByTagName('handlingName')
        show_log(f"Getting SpawnName for {car}, result : {handling_elements[0].firstChild.data.lower()}")
        return handling_elements[0].firstChild.data.lower()

    def get_car_spawn_name2(self, car):
        handling_data = minidom.parse(f'./pakowanko/modify_input/{car}/handling.meta')
        handling_elements = handling_data.getElementsByTagName('handlingName')
        show_log(f"Getting SpawnName for {car}, result : {handling_elements[0].firstChild.data.lower()}")
        return handling_elements[0].firstChild.data.lower()


    def save_paczka_data(self):
        with open('./pakowanko/output/pakowanko_data.json', 'w') as f:
            json.dump(self.data, f, indent=4)
        show_log("Writing Package data.json to ./output/pakowanko_data.json")
        return True

    def load_pack_data(self):
        self.pack_path = "./pakowanko/pack_to_modify"
        self.data = {}
        with open(f"{self.pack_path}/pakowanko_data.json", 'r') as f:
            self.data = json.load(f)
        return self.data
    
    def save_pack_data(self):
        self.pack_path = "./pakowanko/pack_to_modify"
        with open(f"{self.pack_path}/pakowanko_data.json", 'w') as f:
            json.dump(self.data, f, indent=4)
        return True

    def delete_car_from_pack(self, car):
        data = self.data
        car_stream_path = f"./pakowanko/pack_to_modify/data/{data[car]['model']}"
        car_handling_path = f"./pakowanko/pack_to_modify/stream/{data[car]['model']}"
        shutil.rmtree(car_stream_path)
        shutil.rmtree(car_handling_path)
        print(self.data.pop(car))
        i = 0
        for l_car in self.data['carlist']:
            if not l_car == car:
                i += 1
            else:
                print(self.data['carlist'].pop(i))
        self.save_pack_data()
    def init_load_new_cars(self):
        if os.path.exists(f"./pakowanko/modify_input"):
            shutil.rmtree(f"./pakowanko/modify_input")
            show_log("Removing existing modify_input for adding new cars")
            os.mkdir(f"./pakowanko/modify_input")
            show_log("Creating modify_input for adding new cars")
        else:
            os.mkdir(f"./pakowanko/modify_input")
            show_log("Creating modify_input for adding new cars")
    def refresh_new_cars(self):
        files = []
        if os.path.exists(f"./pakowanko/modify_input"):
            files = os.listdir('./pakowanko/modify_input')
        return files

    def add_car_to_pack(self, car_to_add):
        self.load_pack_data()
        for car in self.data['carlist']:
            if car == car_to_add:
                return
        if os.path.exists(f"./pakowanko/modify_input/{car_to_add}"):
            self.data[car_to_add] = {
                "model": car_to_add,
                "spawnname": self.get_car_spawn_name2(car_to_add),
                "files": {
                    "handling": [],
                    "stream": []
                }
            }
            self.data['carlist'].append(car_to_add)
            files = os.listdir(f"./pakowanko/modify_input/{car_to_add}")
            stream_files = os.listdir(f"./pakowanko/modify_input/{car_to_add}/stream")
            handling_data = []
            for file in files:
                if file.endswith('.meta'):
                    handling_data.append(file)
            self.data[car_to_add]["files"]['handling'] = handling_data
            self.data[car_to_add]["files"]['stream'] = stream_files
            car_files = handling_data
            if os.path.exists(f"./pakowanko/pack_to_modify/data/{car_to_add}"):
                shutil.rmtree(f"./pakowanko/pack_to_modify/data/{car_to_add}")
                show_log(f"Removing existing folder for handling data of {car_to_add}")
                os.mkdir(f"./pakowanko/pack_to_modify/data/{car_to_add}")
                show_log(f"Creating folder for handling data of {car_to_add}")
            else:
                os.mkdir(f"./pakowanko/pack_to_modify/data/{car_to_add}")
                show_log(f"Creating folder for handling data of {car_to_add}")
            for handling_file in car_files:
                shutil.copy(f"./pakowanko/modify_input/{car_to_add}/{handling_file}", f"./pakowanko/pack_to_modify/data/{car_to_add}/{handling_file}")
            car_files = stream_files
            if os.path.exists(f"./pakowanko/pack_to_modify/stream/{car_to_add}"):
                show_log(f"Removing existing folder for stream textures of {car_to_add}")
                shutil.rmtree(f"./pakowanko/pack_to_modify/stream/{car_to_add}")
                show_log(f"Creating folder for stream textures of {car_to_add}")
                os.mkdir(f"./pakowanko/pack_to_modify/stream/{car_to_add}")
            else:
                os.mkdir(f"./pakowanko/pack_to_modify/stream/{car_to_add}")
            for stream_file in car_files:
                shutil.copy(f"./pakowanko/modify_input/{car_to_add}/stream/{stream_file}", f"./pakowanko/pack_to_modify/stream/{car_to_add}/{stream_file}")
                show_log(f"Copying {car_to_add}/{stream_file} to stream textures of {car_to_add}")
            self.save_pack_data()
        print(self.data)
            
pk = Pakowanko()

@eel.expose
def open_folder(path):
    os.startfile(os.getcwd()+path)

@eel.expose
def hello():
    print("Hello world!")

@eel.expose
def getPojazdy():
    pojazdy = pk.get_input_content()
    innerhtml = ""
    for pojazd in pojazdy:
        innerhtml += f"""
            <tr>
                <td style="width: 495px;" class="mdl-data-table__cell--non-numeric">{pojazd}</td>
            </tr>
        """
    eel.updatePojazdy(innerhtml)

@eel.expose
def loadPack():
    pojazdy = pk.load_pack_data()['carlist']
    innerhtml = ""
    for pojazd in pojazdy:
        innerhtml += f"""
            <tr>
                <td style="width: 495px;" class="mdl-data-table__cell--non-numeric">{pojazd}</td>
                <td style="width: auto;" class="mdl-data-table__cell--non-numeric">
                    <button value="{pojazd}" id="remove_car_button" class="mdl-button mdl-js-button mdl-button--icon">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>       
        """
    eel.updatePojazdy2(innerhtml)

@eel.expose
def delCar(car):
    pk.delete_car_from_pack(car)

@eel.expose
def getNewCars():
    innerhtml = ""
    for car in pk.refresh_new_cars():
        innerhtml += f"""<option value="{car}">{car}</option>"""
    return innerhtml

@eel.expose
def addCarToPack(car):
    pk.add_car_to_pack(car)

@eel.expose
def startPacking():
    eel.setProgress(10)
    pk.get_input_content()
    eel.sleep(random.randint(1,3))
    eel.setProgress(30)
    pk.process_handling_files()
    eel.sleep(random.randint(1,3))
    eel.setProgress(50)
    pk.process_stream_files()
    eel.sleep(random.randint(1,3))
    eel.setProgress(80)
    pk.init_resource_file()
    eel.sleep(random.randint(1,3))
    eel.setProgress(90)
    pk.save_paczka_data()
    eel.sleep(random.randint(1,3))
    eel.setProgress(100)
    eel.Notify("Process Complete!")
    open_folder('/pakowanko/output')

@eel.expose
def close():
    sys.exit()
    raise SystemExit


eel.init('gui') 
eel.start('index.html', size=(540, 780))
