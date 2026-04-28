import copy
import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0
        # dati da db
        self._situazioni = model.getAllSituazioni()
        # soluzioni sequenza
        self._soluzioni_sequenza = {}


    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()

        if self._mese == 0:
            (self._view.create_alert
             ("Attenzione, selezionare un mese."))
            self._view.update_page()
            return

        if not len(self._situazioni):
            self._view.lst_result.controls.append(
                ft.Text(f"Nessuna situazione trovata per questo mese."))
            self._view.update_page()
            return

        self._view.lst_result.controls.append(
            ft.Text(f"L'umidità media del mese selezionato è:"))

        localita, result = self.situazioni_del_mese(False)

        # calcolo l'umidità media per localita
        for l in localita:
            somma = 0
            contatore = 0
            for r in result:
                if r.localita == l:
                    somma += r.umidita
                    contatore += 1
            self._view.lst_result.controls.append(
                ft.Text(f"{l}: {somma / contatore}"))

        self._view.update_page()


    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()

        if self._mese == 0:
            (self._view.create_alert
             ("Attenzione, selezionare un mese."))
            self._view.update_page()
            return

        if not len(self._situazioni):
            self._view.lst_result.controls.append(
                ft.Text(f"Nessuna situazione trovata per questo mese."))
            self._view.update_page()
            return

        localita, result = self.situazioni_del_mese(True)
        result.sort(key=lambda x: x.data.day)

        self.calcola_percorsi(result)
        valore_ottimo = min(self._soluzioni_sequenza)
        percorso_ottimo = self._soluzioni_sequenza[valore_ottimo]

        self._view.lst_result.controls.append(
            ft.Text(f"La sequenza ottima ha valore {valore_ottimo}"))

        for r in percorso_ottimo:
           self._view.lst_result.controls.append(ft.Text(r))

        self._view.update_page()


    def read_mese(self, e):
        self._mese = int(e.control.value)


    def situazioni_del_mese(self, primi):
        # seleziono le giornate del mese
        result = []
        localita = []
        for s in self._situazioni:
            if s.data.month == self._mese:
                if not primi:
                    result.append(s)
                else:
                    if 1 <= s.data.day <= 15:
                        result.append(s)
            if s.localita not in localita:
                localita.append(s.localita)
        return localita, result


    def calcola_percorsi(self, result):
        self._soluzioni_sequenza.clear()
        self.ricorsione(result, [], 0, 0, 0, 0, 1)


    def ricorsione(self, da_percorrere, percorso, costo,
                   torino_cnt, milano_cnt, genova_cnt, giorno):

        if giorno == 16:
            self._soluzioni_sequenza[costo] = percorso

        else:

            costo_aggiuntivo = 0
            cambio = False
            rimango = False

            # seleziono i posti possibilmente visitabili della giornata
            possibili = []
            for elem in da_percorrere:
                if elem.data.day == giorno:
                    possibili.append(elem)
                else:
                    break

            for i in range(len(possibili)):
                da_percorrere.pop(0)

            # controllo se devo rimanere scegliere una città a caso
            if len(percorso) == 0:
                pass
            # se devo cambiare città
            elif len(percorso) >= 3 and percorso[-1].localita == percorso[-2].localita == percorso[-3].localita:
                cambio = True
            # se devo rimanere nella mia città
            else:
                rimango = True

            for possibile in possibili:

                # cambio città
                if cambio == True and possibile.localita != percorso[-1].localita:
                    costo_aggiuntivo += 100
                # rimango nella città
                elif rimango == True and possibile.localita == percorso[-1].localita:
                    pass
                # sono nella prima città
                elif rimango == False and cambio == False:
                    pass
                else:
                    continue

                if possibile.localita == "Torino":
                    if torino_cnt > 5:
                        continue
                    else:
                        torino_cnt += 1
                elif possibile.localita == "Milano":
                    if milano_cnt > 5:
                        continue
                    else:
                        milano_cnt += 1
                elif possibile.localita == "Genova":
                    if genova_cnt > 5:
                        continue
                    else:
                        genova_cnt += 1

                percorso.append(possibile)
                da_percorrereC = copy.deepcopy(da_percorrere)
                percorsoC = copy.deepcopy(percorso)

                self.ricorsione(da_percorrereC, percorsoC, costo + possibile.umidita + costo_aggiuntivo,
                                torino_cnt, milano_cnt, genova_cnt, giorno + 1)

                if cambio is True:
                    costo -= costo_aggiuntivo

                percorso.remove(possibile)

                if possibile.localita == "Torino":
                    torino_cnt -= 1
                elif possibile.localita == "Milano":
                    milano_cnt -= 1
                else:
                    genova_cnt -= 1

            for i in possibili:
                da_percorrere.insert(0, i)