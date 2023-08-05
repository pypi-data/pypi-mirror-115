""" Модуль, содержащий основной класс GCoreQDK, являющийся носителем всех
методов для взаимодействия с Gravity Compound. Используется как графическим
интерфейсом весовщика, так и WServer."""
from qdk.main import QDK


class GCoreQDK(QDK):
    """ Главный класс, содержащий все методы для взаимодействия с GCore """
    def __init__(self, host_ip, host_port, host_login='login',
                 host_password='pass', *args, **kwargs):
        super().__init__(host_ip, host_port, host_login, host_password,
                         *args, **kwargs)

    def start_round(self, car_number, course, car_choose_mode,
                    dlinnomer=False, polomka=False,
                    carrier=None, trash_cat=None, trash_type=None, notes=None,
                    operator=None, duo_polygon=None):
        """ Отдать команду на начало раунда взвешивания """
        self.execute_method('start_weight_round', car_number=car_number,
                            course=course, car_choose_mode=car_choose_mode,
                            spec_protocol_dlinnomer_bool=polomka,
                            spec_protocol_polomka_bool=dlinnomer,
                            carrier=carrier, trash_cat=trash_cat,
                            trash_type=trash_type, notes=notes,
                            operator=operator, duo_polygon=duo_polygon)

    def get_status(self):
        """ Вернуть состояние готовности весовой площадки (True|False) """
        self.execute_method('get_status')

    def add_comment(self, record_id: int, comment: str):
        """
        Добавить комментарий к существующей записи.
        :param record_id: id записи
        :param comment: добавочный комментарий
        :return:
        """
        self.execute_method('add_comment', record_id=record_id,
                            comment=comment)

    def change_opened_record(self, record_id: int, car_number: str = None,
                             carrier: int = None, trash_cat_id: int = None,
                             trash_type_id: int = None, comment: str = None,
                             polygon: int = None, auto_id: int = None):
        """
        Изменить запись. Можно менять все основные параметры.
        :param record_id: ID этой записи
        :param car_number: Гос.номер, на который надо поменять (если такой
        машиныинет, она будет зарегана, в любом случае,
        в записи будет отображаться только ссылка на это авто.
        :param carrier: ID перевозчика
        :param trash_cat_id: ID категории груза
        :param trash_type_id: ID вида груза
        :param comment: комментарий, который нужно поменять
        :param polygon: Полигон
        :param auto_id: Можно указать ID авто напямую (но, как правило, через
        графический интерфейс поступает гос.номер в виде строки
        (см. car_number))
        :return:
        """
        self.execute_method('change_opened_record', record_id=record_id,
                            car_number=car_number, carrier=carrier,
                            trash_cat_id=trash_cat_id,
                            trash_type_id=trash_type_id, comment=comment,
                            polygon=polygon, auto_id=auto_id)

    def close_opened_record(self, record_id: int):
        """
        Закрыть открытую запись (у которой есть только брутто)
        :param record_id: ID этой записи
        :return:
        """
        self.execute_method('close_opened_record', record_id=record_id)

    def get_unfinished_records(self):
        """
        Вернуть список, содержащий словари, каждый из которых описывает заезд,
        который еще не завершен (без тары)
        :return:
        """
        self.execute_method('get_unfinished_records')

    def get_history(self, time_start=None, time_end=None, trash_cat=None,
                    trash_type=None, carrier=None, auto_id=None, polygon=None,
                    alerts=None, what_time='time_in'):
        """
        Получить историю заездов. Если ни один аргумент не указан, то вернется
        история за сегодняшний день, без каких либо фильтров. Указанные же
        аргументы - это фильтры, они суммируются в любом порядке и количестве.
        :param time_start: с какой даты учитывать
        :param time_end: по какую дату учитывать
        :param trash_cat: фильтрация по категории груза
        :param trash_type: фильтрация по виду груза
        :param carrier: фильтрация по перевозчику
        :param auto_id: фильтрация по авто
        :param polygon: фильтрация по объекту-приемщику
        :param alerts: фильтрация по наличию алертов
        :param what_time: какую дату брать за учетную (time_in|time_out).
        То есть, time_start и time_end могут быть как время въезда, так и
        время выезда (по умолчанию, это время въезда)
        :return:
        """
        self.execute_method('get_history', time_start=time_start,
                            time_end=time_end, trash_cat=trash_cat,
                            trash_type=trash_type, carrier=carrier,
                            auto_id=auto_id, polygon=polygon,
                            alerts=alerts, what_time=what_time)

    def get_table_info(self, table_name: str, only_active=True):
        """
        Вернуть данные о таблице из wdb.
        Внимание! Не все таблицы доступны, как и не все поля, доступ по
        таблице происходит из белого списка, а по полям, не отправляются те
        поля, которые отмечены в черном списке (например, поле users.password).
        Механизм допуска прописан в модуле gravity_data_worker.
        :param table_name: Название нужной таблицы
        :param only_active: Возвращать ли только те поля, у которых поле active
        положительно?
        :return:
        """
        self.execute_method('get_table_info', tablename=table_name,
                            only_active=only_active)

    def get_last_event(self, auto_id: int):
        """
        Получить данные о последнем заезде авто с ID (auto_id)
        :param auto_id: ID авто, по котором нужна информация
        :return: Возвращает словарь с данными о заезде
        """
        self.execute_method('get_last_event', auto_id=auto_id)

    def open_external_barrier(self):
        """
        Открыть внешний шлагбаум
        :return:
        """
        self.operate_barrier(barrier_name='EXTERNAL_GATE', operation='open')

    def close_external_barrier(self):
        """
        Закрыть внешний шлагбаум
        :return:
        """
        self.operate_barrier(barrier_name='EXTERNAL_GATE', operation='close')

    def open_internal_barrier(self):
        """
        Открыть внешний шлагбаум
        :return:
        """
        self.operate_barrier(barrier_name='INTERNAL_GATE', operation='open')

    def close_internal_barrier(self):
        """
        Закрыть внешний шлагбаум
        :return:
        """
        self.operate_barrier(barrier_name='INTERNAL_GATE', operation='close')

    def operate_barrier(self, barrier_name: str, operation: str):
        """
        Произвести работу со шлагбаумами (открыть или закрыть)
        :param barrier_name: Название шлагбаума. Обычно он носит вид,
        типа "НАПРАВЛЕНИЕ_ИМЯ" (EXTERNAL_BARRIER)
        :param operation: (close|open) Открыть или закрыть шлагбаум
        :return:
        """
        self.execute_method('operate_gate_manual_control',
                            barrier_name=barrier_name,
                            operation=operation)

    def try_auth_user(self, username: str, password: str):
        """ Попытка аутентификации весовщика через графический интерфейс
        :param username: Логин пользователя
        :param password: Пароль пользователя
        :return: Возвращает либо {'status'"""
        self.execute_method('try_auth_user', username=username,
                            password=password)

    def capture_gui_launched(self):
        """ Зафиксировать запуск графического интерфейса в логе """
        self.execute_method('capture_cm_launched')

    def capture_gui_terminated(self):
        """ Зафиксировать отключение графического интерфейса в логе """
        self.execute_method('capture_cm_terminated')

    def restart_core(self):
        """ Перезапустить Gravity Core Compound """
        self.execute_method('restart_core')

    def add_carrier(self, name, inn=None, kpp=None, ex_id=None, status=None,
                    wserver_id=None):
        """
        Добавить нового перевозчика
        :param name: Название перевозчика
        :param inn: ИНН перевозчика
        :param kpp: КПП перевозчика
        :param ex_id: ID перевозчика из внешней системы (например, 1С)
        :param status: Статус (действующий/недействующий)
        :param wserver_id: ID перевозчика в базе GDB
        :return:
        """
        self.execute_method('add_new_carrier', name=name, inn=inn, kpp=kpp,
                            ex_id=ex_id, status=status, wserver_id=wserver_id)

    def add_auto(self, car_number, wserver_id, model, rfid, id_type,
                 rg_weight):
        """
        Добавить новое авто
        :param car_number: Гос.номер авто
        :param wserver_id: ID авто из базы GDB
        :param model: Модель авто
        :param rfid: RFID номер авто
        :param id_type: Протокол авто
        :param rg_weight: Справочный вес тары авто
        :return:
        """
        self.execute_method('add_auto', car_number=car_number, model=model,
                            rfid=rfid, id_type=id_type, rg_weight=rg_weight,
                            wserver_id=wserver_id)

    def add_trash_cat(self, cat_name, wserver_id):
        """
        Добавить новую категорию груза
        :param cat_name: Название категории груза
        :param wserver_id: ID из базы GDB
        :return:
        """
        self.execute_method('add_trash_cat', cat_name=cat_name,
                            wserver_id=wserver_id)

    def add_trash_type(self, type_name, wserver_id, wserver_cat_id):
        """
        Добавить новый вид груза
        :param type_name: Название вида груза
        :param wserver_id: ID вида груза из GDB
        :param wserver_cat_id: ID категории груза из GDB, за которым закреплен
        вид груза
        :return:
        """
        self.execute_method('add_trash_type', type_name=type_name,
                            wserver_cat_id=wserver_cat_id,
                            wserver_id=wserver_id)

    def add_operator(self, full_name, username, password, wserver_id):
        """
        Добавить нового пользователя (весовщика)
        :param full_name: Полное имя (ФИО)
        :param username: Логин пользователя
        :param password: Пароль пользователя
        :param wserver_id: его ID из базы GDB
        :return:
        """
        self.execute_method('add_operator', full_name=full_name,
                            username=username, password=password,
                            wserver_id=wserver_id)

    def get_record_info(self, record_id: int):
        """
        Получить информацию о заезде по его ID
        :param record_id: ID записи
        :return: {ID: int, auto: auto_id, time_in: date, ...}
        """
        self.execute_method('get_record_info', record_id=record_id)

    def get_auto_info(self, car_number: str = None, auto_id: int = None):
        """
        Вернуть информацию об авто по его гос.номеру
        :param auto_id: Идентификатор авто
        :param car_number: Гос. номер авто
        :return:
        """
        self.execute_method('get_auto_info', car_number=car_number,
                            auto_id=auto_id)
