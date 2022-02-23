class ExamException(Exception): #classe per le eccezioni
  pass

class CSVTimeSeriesFile(): #controlla esistenza file_csv
  def __init__(self, name):
    # controllo che name sia una stringa
    if not isinstance(name, str):
      raise ExamException("Errore, il parametro name non è una stringa!")

    # salvo name nella variabile istanza
    self.name = name

  def get_data(self):
    # controllo che il file esista e sia leggibile
    try:
      file_csv = open(self.name, 'r')
    except:
      raise ExamException('File non esiste!')

    time_series = [] 

    # analizzo il file
    for line in file_csv:
        line = line.split(',')
        # controllo che ci sia la data e numero di passeggeri
        if len(line) == 2: 
          date = line[0]
          passengers = line[1]
          
          # controllo che la data sia in formato anno-mese
          date = date.split('-')
          if len(date) >= 2:
            year = date[0]
            month = date[1]
            # controllo che l'anno, il mese e il numero di passeggeri siano validi
            try:
              year = int(year)
              month = int(month)
              passengers = int(passengers)
            except:
              continue # ignoro la riga del csv
            # l'anno deve essere positivo e il mese compreso tra 1 e 12
            if year >= 0:
              if 1 <= month <= 12:
                # controllo che il numero di passeggeri sia positivo
                if passengers >= 0:
                  # controllo che la time_series sia ordinata e senza duplicati
                  if len(time_series) > 0:
                    # prendo la data dell'ultimo elemento inserito nella variabile time_series
                    prev_date = time_series[-1][0]
                    prev_date = prev_date.split('-')
                    prev_year = int(prev_date[0])
                    prev_month = int(prev_date[1])
                    if prev_year <= year:
                        if prev_year == year:
                          if prev_month >= month:
                            raise ExamException("time_series ha duplicati o non è ordinata")
                    else: 
                      raise ExamException("time_series ha duplicati o non è ordinata")
                  
                  # aggiungo time_stamp appena analizzato nell'array time_series
                  time_series.append([f"{year}-{str(month).zfill(2)}", passengers]) #inserisco in coda gli elementi 

    # chiudo il file
    file_csv.close()
    return time_series

#definisco metodo per variazione tra coppie di mesi quasi uguali
def detect_similar_monthly_variations(time_series, years): 
    # controllo che ci sia almeno un mese per anno scelto
    presenti1 = 0 #passeggeri anno 1
    presenti2 = 0 #passeggeri anno 2
    
    #analizzo tutti i mesi e controllo che ci siano passeggeri
    for i in range (1, 12): 
        if get_passengers(time_series, years[0], i) > 0:
            presenti1 = presenti1 + 1
        if get_passengers(time_series, years[1], i) > 0:
            presenti2 = presenti2 + 1
    if presenti1 == 0 or presenti2 == 0:
        raise ExamException("Errore, uno dei due anni non esiste!")

    result = []
    
    # scorro i mesi
    for i in range(1, 12):
        passNextMonthYear1 = get_passengers(time_series, years[0], i + 1)
        passCurrentMonthYear1 = get_passengers(time_series, years[0], i)

        if passNextMonthYear1 == -1 or passCurrentMonthYear1 == -1:
          result.append('False')
          continue

        diffPassYear1 = passNextMonthYear1 - passCurrentMonthYear1

        passNextMonthYear2 = get_passengers(time_series, years[1], i + 1)
        passCurrentMonthYear2 = get_passengers(time_series, years[1], i)

        if passNextMonthYear2 == -1 or passCurrentMonthYear2 == -1:
          result.append('False')
          continue

        diffPassYear2 = passNextMonthYear2 - passCurrentMonthYear2

        if abs(diffPassYear1 - diffPassYear2) <= 2:
          result.append('True')
        else:
          result.append('False')

    return result
    
def get_passengers(time_series, yearIn, monthIn): #controlla che ci siano paseggieri in un dato anno e mese
    result = -1 #non trova passeggeri 

    for time_stamp in time_series:
        date = time_stamp[0].split('-') #suddivido date
        year = int(date[0])
        month = int(date[1])
        passengers = time_stamp[1]

        if year == yearIn and monthIn == month:
            result = int(passengers)
            break
        
    return result