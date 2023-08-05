""" Модуль, хранящий все функции, производящие проверку раунда взвшеивания на алерты """
from gravityRecorder.alerts import settings as s


def check_car_choose_mode(rfid, alerts, choose_mode, course, *args, **kwargs):
    # Проверить, как была выбрана машина (вручную/автоматоически)
    if choose_mode.lower() == 'manual' and not s.alerts_description['manual_pass']['description'] in alerts:
        # Если выбрали вручную и алерта еще нет
        try:
            if not rfid and not s.alerts_description['no_rfid']['description'] in alerts:
                # Если нет RFID, возбудить алерт, что машина привезла ТКО, но без метки
                alerts += s.alerts_description['no_rfid']['description']
            else:
                # Если же метка есть, возбудить алерт, что выбрали вручную машину с меткой
                full_alert = s.alerts_description['manual_pass']['description'].format(
                    s.skud_courses_description[course]['description'])
                alerts += full_alert
        except:
            pass
    return alerts


def cargo_null(cargo, alerts):
    # Проверить, не околонулевое ли нетто, если да - дополнить алерт кодом из wsettings и вернуть
    check = s.alerts_description['cargo_null']
    if int(cargo) < check['null']:
        alerts += check['description']
    return alerts


def check_fast_car(last_visit_date, timenow,  alerts):
    # Проверить, не слишком ли быстро вернулась машина, если да - дополнить алерт кодом из wsettings и вернуть
    print('\nИнициирована проверка на FastCar')
    check = s.alerts_description['fast_car']
    return_time = timenow - last_visit_date
    return_time = return_time.seconds
    print('\tВремя возвращения:', return_time)
    print('\tНеобходимо для возбуждения алерта:', check['time'])
    if return_time < check['time'] and not check['description'] in alerts:
        notes = str(int(return_time / 60)) + ' минут после прошлого заезда'
        alerts += check['description'].format(notes)
        print('\t\tАлерт возбужден')
        return alerts
    else:
        print('\t\tАлерт не возбужден')
        return alerts


def add_alert(sqlshell, rec_id, alerts):
    """ Добавить алерт к существующим """
    command = "UPDATE {} SET alerts=alerts || '{}' WHERE id={}".format('records', alerts, rec_id)
    sqlshell.try_execute(command)

