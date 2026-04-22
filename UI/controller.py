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

        self.calcola(result)
        ris_value = min(self._soluzioni_sequenza)
        ris_sequenza = self._soluzioni_sequenza[ris_value]

        self._view.lst_result.controls.append(
            ft.Text(f"La sequenza ottima ha valore {ris_value}"))

        for r in ris_sequenza:
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


    def calcola(self, tutte):
        self.recursion([], tutte, 1, 0, 0, 0, 0)


    def recursion(self, visitate, tutte, giorno, costo, milano_cnt, torino_cnt, genova_cnt):
        # se sono arrivato al giorno 16
        if giorno == 16:
            self._soluzioni_sequenza[costo] = visitate

        else:
            # seleziono le situazioni della giornata di oggi che non siano state già visitate 6 volte
            visitabili = []
            cambio = False
            tutte_c = copy.deepcopy(tutte)

            for t in tutte:
                if t.data.day != giorno:
                    break

                if t.localita == "Genova":
                    tutte_c.pop(0)
                    if genova_cnt < 6:
                        visitabili.append(t)

                elif t.localita == "Milano":
                    tutte_c.pop(0)
                    if milano_cnt < 6:
                        visitabili.append(t)

                elif t.localita == "Torino":
                    tutte_c.pop(0)
                    if torino_cnt < 6:
                        visitabili.append(t)

            # se è la prima che visito posso visitarle tutte
            if len(visitate) == 0:
                pass

            # se ne ho già visitata una tre volte di fila devo cambiare città
            elif len(visitate) >= 3 and visitate[-1].localita == visitate[-2].localita == visitate[-3].localita:
                citta_attuale = visitate[-1].localita
                copia = copy.deepcopy(visitabili)
                cambio = True

                for elem in copia:
                    if elem.localita == citta_attuale:
                        visitabili.remove(elem)

            # non devo cambiare città
            else:
                citta_attuale = visitate[-1].localita
                copia = copy.deepcopy(visitabili)
                for elem in copia:
                    if elem.localita != citta_attuale:
                        visitabili.remove(elem)

            if len(visitabili) > 0:
                self.aggiornamento(visitate, tutte_c, giorno, costo,
                                   milano_cnt, torino_cnt, genova_cnt, visitabili, cambio)

    def aggiornamento(self, visitate, tutte_c, giorno, costo, milano_cnt, torino_cnt, genova_cnt, visitabili, cambio):
        for citta in visitabili:
            visitate_c = copy.deepcopy(visitate)
            visitate_c.append(citta)

            if citta.localita == "Torino":
                if cambio is True:
                    self.recursion(visitate_c, tutte_c, giorno + 1, costo + citta.umidita + 100,
                               milano_cnt, torino_cnt + 1, genova_cnt)
                else:
                    self.recursion(visitate_c, tutte_c, giorno + 1, costo + citta.umidita,
                               milano_cnt, torino_cnt + 1, genova_cnt)

            elif citta.localita == "Milano":
                if cambio is True:
                    self.recursion(visitate_c, tutte_c, giorno + 1, costo + citta.umidita + 100,
                               milano_cnt + 1, torino_cnt, genova_cnt)
                else:
                    self.recursion(visitate_c, tutte_c, giorno + 1, costo + citta.umidita,
                               milano_cnt + 1, torino_cnt, genova_cnt)

            else:
                if cambio is True:
                    self.recursion(visitate_c, tutte_c, giorno + 1, costo + citta.umidita + 100,
                               milano_cnt, torino_cnt, genova_cnt + 1)
                else:
                    self.recursion(visitate_c, tutte_c, giorno + 1, costo + citta.umidita,
                               milano_cnt, torino_cnt, genova_cnt + 1)

