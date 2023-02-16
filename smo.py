import random
rnd=random.randint(1,100)
random.seed(rnd)        # воспроизводимость результатов
time = 0                # глобальное время модели
tranzact_num = 1        # номер транзакта
max_sec = 24            # максимально допустимое между приходами заявок
station_time = [9, 8]
all_time = [random.uniform(0, max_sec), 0, 0] # время текущего транзакта и двух устройств
que = [[], []] # обслуживающие устройства + очередь
log = open('log.txt', 'w') # открытие файла для записи
t_z=0.0 #занял
t_o=0.0 #освободил
t_oz=0.0 #общая занятость
k_zag=0 #коэф загрузки

def min_time(): # поиск минимального времени
    if len(que[0]) == 0 and len(que[1]) == 0: # при нулевых очередях - время поступления заявки 
        return [all_time[0], 0]  
    elif len(que[0]) == 0:  # при отсутствии первой очереди - время поступления либо время второй очереди
        return [min(all_time[0], all_time[2]), all_time.index(min(all_time[0], all_time[2]))]
    elif len(que[1]) == 0: # при отсутствии второй очереди - время поступления либо время первой очереди
        return [min(all_time[0], all_time[1]), all_time.index(min(all_time[0], all_time[1]))]
    else: # если есть обе очереди - минимальное из всех
        local = 0
        local_min = min(all_time)
        for i in all_time:
            if local_min == i:
                local = all_time.index(i)
        return [local_min, local]

def update_stat(i): # обновление состояний
    global tranzact_num
    if i == 0: # минимальное время - время новой заявки
        log.write("В момент времени " + str(time) + " транзакт с идентификатором " + str(tranzact_num) + " вошел в модель\n")
        all_time[0] = random.uniform(0, max_sec)  # обновление времени заявки
        if len(que[0]) <= len(que[1]): # условие на очередь
            que_upd(1)
        else:
            que_upd(2)
        tranzact_num += 1
    else:  # минимальное время - время выхода заявки из одного из устройств
        tranz_upd(i)

def que_upd(i): #   обновление очереди
    global t_z
    if len(que[i-1]) == 0: # заявка сразу идет на обслуживание 
        log.write("В момент времени " + str(time) + " транзакт с идентификатором " +str(tranzact_num) + " занял устройство " + str(i) + "\n")
        if i==1:
          t_z=time
        all_time[i] = random.uniform(station_time[i-1], max_sec) #  обновление времени обслуживания
    else:
        log.write("В момент времени " + str(time) + " транзакт с идентификатором " +str(tranzact_num) + " встал в очередь " + str(i) + "\n")
    que[i-1].append(tranzact_num) # добавляем в очередь номер заявки 

def tranz_upd(i): # обслуживание заявки на устройстве
    global t_oz
    global t_o, t_z
    log.write("В момент времени " + str(time) + " транзакт с идентификатором " +str(que[i-1][0]) + " освободил устройство " + str(i) + "\n")
    if i==1:
      t_o=time
      t_oz+=(t_o-t_z)
    log.write("В момент времени " + str(time) + " транзакт с идентификатором " +str(que[i-1][0]) + " вышел из модели\n")
    que[i-1].pop(0) # удаление заявки из системы
    if len(que[i-1]) > 0: # если есть очередь - обновляем глобальное время устройства
        log.write("В момент времени " + str(time) + " транзакт с идентификатором " +str(que[i-1][0]) + " занял устройство " + str(i) + "\n")
        if i==1:
          t_z=time
        all_time[i] = random.uniform(station_time[i-1], max_sec)  
    else: # если нет - делаем его нулевым
        all_time[i] = 0    

while True:
    minimal = min_time()
    for i in range(3): # обновление времени с учетом найденного минимального.
        if all_time[i] != 0:
            all_time[i] -= minimal[0]
    time += minimal[0] 
    if time > 3600:     
        log.write("Время симуляции, равное 3600 секунд, закончено\n")
        #log.close()
        break
    update_stat(minimal[1])
print(t_oz)
k_zag=t_oz/(3600)
log.write("коэфф загрузки первой кассы: "+str(k_zag))
log.close()