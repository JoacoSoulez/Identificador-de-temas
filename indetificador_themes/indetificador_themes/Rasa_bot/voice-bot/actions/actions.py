# This files contains your custom actions which can be used to run
# custom Python code.

# from cmath import nan
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import pymssql
from rasa_sdk.events import FollowupAction
import re



# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

lista = []
# conn = pymssql.connect(server='192.168.120.120', user='jsoulez', password='Mopc2022*', database='master')
# cur = conn.cursor()
# query = """SELECT top 3 cartera.IDMOROSO, cartera.IDCLIENTE,moroso.NOMBRE, producto.TOTALDEUDA, producto.VALORCUOTA, producto.TOTALPAGOS, producto.FULTPAGO, contabilidad.TIPO, contabilidad.SUBTIPO, contabilidad.DATO FROM Active.dbo.CARTERA as cartera
#             JOIN
#             Active.dbo.MOROSO AS moroso
#             on cartera.IDMOROSO = moroso.IDMOROSO
#             JOIN
#             Active.dbo.PRODUCTO as producto
#             on cartera.IDMOROSO = producto.IDMOROSO
#             JOIN
#             Active.dbo.DAM_CONTACTABILIDAD_FILTRADA AS contabilidad
#             on cartera.IDMOROSO = contabilidad.IDMOROSO
#             where contabilidad.TIPO = 'TEL.CELULAR';"""

# bbdd = pd.read_sql_query(query,conn)
bbdd = pd.read_csv('bbdd.csv')



#datos para la conexion a la DB
# class ActionSQL(Action):
#     def name(self) -> Text:
#         return "action_SQL"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         conn = pymssql.connect(server='192.168.120.120', user='jsoulez', password='Mopc2022*', database='master')
#         cur = conn.cursor()
#         query = """SELECT top 3 cartera.IDMOROSO, cartera.IDCLIENTE,moroso.NOMBRE, producto.TOTALDEUDA, producto.VALORCUOTA, producto.TOTALPAGOS, producto.FULTPAGO, contabilidad.TIPO, contabilidad.SUBTIPO, contabilidad.DATO FROM Active.dbo.CARTERA as cartera
#                     JOIN
#                     Active.dbo.MOROSO AS moroso
#                     on cartera.IDMOROSO = moroso.IDMOROSO
#                     JOIN
#                     Active.dbo.PRODUCTO as producto
#                     on cartera.IDMOROSO = producto.IDMOROSO
#                     JOIN
#                     Active.dbo.DAM_CONTACTABILIDAD_FILTRADA AS contabilidad
#                     on cartera.IDMOROSO = contabilidad.IDMOROSO
#                     where contabilidad.TIPO = 'TEL.CELULAR';"""

#         bbdd = pd.read_sql_query(query,conn)


#         return bbdd

class ActionPrepareToCall(Action):
    def name(self) -> Text:
        return "preparar_slots_por_cliente"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # bbdd = ActionSQL.run(self, CollectingDispatcher,
        #                      Tracker, Dict[Text, Any]
        #                      )

        for n in range(len(bbdd)):
            if bbdd["IDCLIENTE"][0] == 'COTO23              ':
                nombre_entidad = 'COTO'
            else:
                nombre_entidad = str(bbdd["IDCLIENTE"][0]).replace(" ","")

        nombre_entidad = ' '.join(re.sub("([^0-9A-Za-z \t])", " ", nombre_entidad).split())
        monto_adeudado = str(bbdd['TOTALDEUDA'][0])
        nombre_cliente = str(bbdd["NOMBRE"][0]).replace(" ","")
        deuda_minima = bbdd['VALORCUOTA'][0]

        return [
            SlotSet("nombre_entidad", nombre_entidad),
            SlotSet("nombre_cliente", nombre_cliente),
            SlotSet('monto_adeudado', monto_adeudado),
            SlotSet('deuda_minima', deuda_minima),
        ]

class SeleccionEntidad(Action):
    def name(self) -> Text:
        return "action_utter_definicion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        coto = ActionPrepareToCall.run(self, CollectingDispatcher, Tracker, Dict[Text, Any])

        if coto[0] == {'event': 'slot', 'timestamp': None, 'name': 'nombre_entidad', 'value': 'COTO'}:
            print(coto[0])
            return[FollowupAction('action_utter_coto_presentacion')]
        else:
            print(len(lista), coto)
            return[FollowupAction('action_utter_presentacion')]
        # return[]


class ActionPresentacion(Action):
    def name(self) -> Text:
        return "action_utter_presentacion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_presentacion")

        return []

class ActionVerificacionIdentidad(Action):
    def name(self) -> Text:
        return "action_utter_verificacion_identidad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template='utter_verificacion_identidad')

        return []

class ActionVerificacionIdentidad(Action):
    def name(self) -> Text:
        return "action_utter_verificacion_identidad_coto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_verificacion_identidad")

        return [ ]


class ActionInformeDeuda(Action):
    def name(self) -> Text:
        return "action_utter_informe_deuda"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_informe_deuda")

        return [SlotSet("reconoce_identidad", True)]


class ActionPresentacionCoto(Action):
    def name(self) -> Text:
        return "action_utter_coto_presentacion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        dispatcher.utter_message(template="utter_coto_presentacion")

        return []

class ActionDeudaCoto(Action):
    def name(self) -> Text:
        return "action_utter_coto_informe_deuda"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_coto_informe_deuda")

        return [SlotSet("reconoce_identidad", True)]

class ActionVerificacionIdentidadCoto(Action):
    def name(self) -> Text:
        return "action_utter_coto_persona_incorrecta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template='utter_coto_persona_incorrecta')

        return [SlotSet("reconoce_identidad", False)]

class ActionVerificacionIdentidadCoto(Action):
    def name(self) -> Text:
        return "action_utter_persona_incorrecta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template='utter_persona_incorrecta')

        return [SlotSet("reconoce_identidad", False)]


# class ActionRestarted(Action):
#     def name(self):
#         return 'action_restart'
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("Restarted")
#         a = 1
#         lista.append(a)
#         return[Restarted()]
class ActionGoodBye(Action):
    def name(self):
        return 'action_utter_goodbye'
    def run(self, dispatcher, tracker, domain):
        a = 1
        lista.append(a)
        dispatcher.utter_message(template="utter_goodbye")
        # coto = ActionPrepareToCall.run(self, CollectingDispatcher, Tracker, Dict[Text, Any])
        #df = pd.DataFrame(coto)
        reconoce_identidad = ActionInformeDeuda.run(self, CollectingDispatcher, Tracker, Dict[Text, Any])
        reconoce_identidad_coto = ActionVerificacionIdentidadCoto.run(self, CollectingDispatcher, Tracker, Dict[Text, Any])
        print(reconoce_identidad, reconoce_identidad_coto )
        # if reconoce_identidad ==
        # df['reconoce_identidad']  = ActionInformeDeuda.run(self, CollectingDispatcher, Tracker, Dict[Text, Any]).get('value')
        # ActionVerificacionIdentidadCoto
        # df.to_csv(index=False)
        return[]
