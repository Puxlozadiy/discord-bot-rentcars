access_list = [
    #Rico Access
    [
        [284218293601042433, 917122080129032213, 916563929612820512, 0, 'Rico'], # ID, log_channel, money_channel, owner_num, name
        ['777', '222', '666', '605', '394']
    ],
    #Hurick Access
    [
        [471247102438277131, 917122080129032213, 916563929612820512, 1, 'Hurick'],
        []
    ],
    #Nick Access
    [
        [473489623847534592, 923207262527443035, 923215838675341333, 2, 'Nick'],
        ['302']
    ],
    #Kapsul Access
    [
        [467594732906741763, 923271315270549574, 923275886697021500, 3, 'Kapsul'],
        ['433', '130', '457', '347', '856', '658', '327']
    ],
    #Conqueror Access
    [
        [514033628297035791, 923882354685124658, 923882650417115177, 4, 'Conqueror'],
        ['696', '969']
    ],
    #Tovsali Access
    [
        [419869045203140618, 924437479736610897, 924437573898731600, 5, 'Tovsali'],
        ['336', '127']
    ],
    #Crystal Access
    [
        [790343763637043300, 925490072067928136, 925490235230539908, 6, 'Crystal'],
        ['223']
    ],
    #Slayer Access
    [
        [469858564299816960, 925681061713825842, 925681109705031752, 7, 'Slayer'],
        ['344', '648']
    ],
    #Crazy Access
    [
        [775417780421001237, 926192748225245246, 926192818093965333, 8, 'Crazy'],
        ['101', '102', '103', '104']
    ],
]



def getLogChannel(user_id):
    log_channel = 0
    for user in access_list:
        userid = user[0][0]
        if user_id == userid:
            log_channel = user[0][1]
            break
    return log_channel


def getAccess(user_id, car_name):
    getAccess = 0
    owner = -1
    for user in access_list:
        userid = user[0][0]
        if user_id == userid:
            for cars in user[1]:
                if car_name == cars:
                    getAccess = 1
                    owner = user[0][3]
                    break
    list = [getAccess, owner]
    return list

def getId(car_name):
    user_id = 0
    for user in access_list:
        for cars in user[1]:
            if car_name == cars:
                user_id = user[0][0]
                break
    return user_id

def chooseCar(car_name):
    chooseCar = -1
    if car_name == 'Ford Raptor':
        chooseCar = 1
    if car_name == 'Lamborghini Urus':
        chooseCar = 2
    if car_name == 'Mercedes-G63 6x6':
        chooseCar = 3
    if car_name == 'Infinity FX50s':
        chooseCar = 4
    if car_name == 'Rolls-Royce Cullinan':
        chooseCar = 5
    if car_name == 'Rolls-Royce Ghost':
        chooseCar = 6
    if car_name == 'Buggati Chiron':
        chooseCar = 7
    if car_name == 'McLaren Senna':
        chooseCar = 8
    if car_name == 'McLaren 720s':
        chooseCar = 9
    if car_name == 'Ferrari Aperta':
        chooseCar = 10
    if car_name == 'Pagani Huayra':
        chooseCar = 11
    if car_name == 'BMW X6M':
        chooseCar = 12
    if car_name == 'Cadillac ECTO-1':
        chooseCar = 13
    return chooseCar