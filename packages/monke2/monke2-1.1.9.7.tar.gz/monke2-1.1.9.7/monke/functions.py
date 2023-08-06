import numpy as np

def roundup(x,r=2):
        a = x*10**r
        a = np.ceil(a)
        a = a*10**(-r)

        if type(x) == float or type(x) == int or type(x) == np.float64:
            if a == 0 :
                a=10**(-r)
        else:
            try:                                           # rundet mehrdimensionale arrays
                for i,j in enumerate(a):
                    for k,l in enumerate(j):
                        if i == 0:  
                            i=10**(-r)
            except:                                        # rundet eindimensionale arrays
                for i,j in enumerate(a):
                    if i == 0:  
                        i=10**(-r)
                    
        return np.around(a,r)

def varianz_xy(x,x_mean,y,y_mean):
        return (1/len(x))*((x-x_mean)*(y-y_mean)).sum()

def varianz_x(x,x_mean):
    return (1/len(x))*((x-x_mean)**2).sum()
    
def mittel_varianzgewichtet(val,val_err):
    return (val/(val_err**2)).sum()/(1/(val_err**2)).sum()


# Passt die Rundung von Werten an die Fehler an, erzeugt strings fertig für tabellen--üBERFLÜSSIG! WURDE ERSETZT DURCH error_round
def errorRound(x, xerr):
    print('veraltet: benutze stattdessen error_round()')
    new_x = [0]*len(x)
    new_x_err = [0]*len(x)
    err_str = [0]*len(x)
    if len(x) == len(xerr):
        for i in range(len(x)):
            floatxerr = xerr.astype(np.float64)                             # ändert type zu float64, weil roundup funktion nicht mit int funktioniert
            errstring = np.format_float_positional(xerr[i])                 # Fehler als String

            #-- rundet Fehler ---
            k = 0
            while (errstring[k] != '.'):
                k += 1
            if (errstring[0] == '1' or errstring[0] == '0'):
                k -= 1
            if errstring[0] == '1' and k == 0:

                new_x_err[i] = roundup(floatxerr[i],1)      # rundet einstelligen Zahlen

                if int(new_x_err[i]) == new_x_err[i]:
                    new_x_err[i] = int(new_x_err[i])   # falls ganzzahlig wird zu int konvertiert
                else:
                    k += 1

            elif (k != 0):
                k = -k
                new_x_err[i] = int(roundup(floatxerr[i],k+1))   # rundet alle Zahlen > 1 auf
                if errstring[0] == '1' and str(new_x_err[i])[0] != '1':
                    k -= 1

            else:
                #print('float',new_x_err[i])
                k = 2                                          # rundet fließkommazahlen < 1
                
                while errstring[k] == '0':
                    k += 1
                k -= 1
                if errstring[k+1] == '1' and round(xerr[i],k) != xerr[i]:
                    new_x_err[i] = roundup(floatxerr[i],k+1)
                    k += 1
                else:
                    new_x_err[i] = roundup(floatxerr[i],k)
                
                errstring = np.format_float_positional(new_x_err[i])
                k = len(errstring) - 2
               
                if new_x_err[i] == int(new_x_err[i]):
                    k = 0                                      # setzt rundungsstelle auf 0, wenn fehler auf 1 gerundet wird
            err_str[i] = np.format_float_positional(new_x_err[i])  
            
            if new_x_err[i] == int(new_x_err[i]):
                err_str[i] = str(int(new_x_err[i]))
                new_x_err[i] = int(new_x_err[i])

            #print(k)
            #--passt nachkommastelle der werte an fehler
            errstring = np.format_float_positional(new_x_err[i])     
            
            if k >= 0:
                new_x[i] = round(x[i],k)
                numformat = '{:.'+str(k)+'f}'
                new_x[i] = numformat.format(new_x[i])
            else:
                new_x[i] = round(x[i],k+1)
                numformat = '{:.'+str(0)+'f}'
                new_x[i] = str(int(new_x[i]))
        
    else:
        print('errorRound: arrays must have same length')

    return new_x, err_str

def error_round(x, xerr):

    xerr_sci = [0]*len(x)
    new_xerr = [0]*len(x)
    xerr_str = ['']*len(x)         # gerundete werte als string
    new_x = [0]*len(x)
    x_str = ['']*len(x)

    for i, j in enumerate(xerr):
        xerr_sci[i] = np.format_float_scientific(j)
        this = xerr_sci[i]
        K = ''               # gibt Rundungsstellen an
        last = len(this) -1  # letzer index
        K = this[last-2:]
        K = -int(K)
        if this[0] == '1':
            K +=1
        
        new_xerr[i] = roundup(xerr[i],K)
        xerr_str[i] = np.format_float_positional(new_xerr[i])
        if new_xerr[i] == int(new_xerr[i]):           
            new_xerr[i] = int(new_xerr[i])                  # transformier ganzzahlige floats in ints
            xerr_str[i] = str(new_xerr[i])


        # definiere neues K bei gerundeten Fehlern
        xerr_sci[i] = np.format_float_scientific(new_xerr[i])
        this = xerr_sci[i]
        K = ''               # gibt Rundungsstellen an
        last = len(this) -1  # letzer index
        K = this[last-2:]
        K = -int(K)
        if this[0] == '1' and (this[2] != 'e'):
            K +=1

        # Runde Messwerte
        new_x[i] = round(x[i],K)
        if K >= 0:
            numformat = '{:.'+str(K)+'f}'
            x_str[i] = numformat.format(new_x[i])
        else:
            x_str[i] = str(int(new_x[i]))

        if x_str[i][0] == '-' and new_x[i] == 0:                # entfernt bei -0.0 das minuszeichen
            new_x[i] = -new_x[i]
            x_str[i] = x_str[i][1:]

    return x_str, xerr_str
# Erstellt Wertetabellen, die in LaTeX eingefügt werden können
def make_table(array,header ='',align = '',latex=True):
    try:
        from texttable import Texttable
        from latextable import draw_latex
    except:
        print('error: für make_table müssen die Pakete texttable und latextable installiert werden')

    num = len(array)                        # Anzahl der Spalten

    try:
        length = np.shape(array[0])[1]                 # Anzahl der Reihen, falls erstes Element 2d ist
    except:
        length = len(array[0])                          # Anzahl der Reihen, falls erstes Element 1d ist
        
    if align == '':                                                     
        align = ['c'] * num
    if header == '':
        list = [0] * num
        for i in range (num):
            list[i] = str(i+1)
        header = list
    
    if len(align) != len(header) or len(header) != len(array):                                  # kontroliiert die Dimensionen der Listen
        print('error: align und header und array benötigen die selben Dimensionen')
        return
    

    k = np.zeros(num)
    for i,j in enumerate(array):             # gibt k = 2, wenn as Array 2-dim ist, k = 1 für 1-dim arrays
        try:
            k[i] = np.shape(j)[1]
            k[i] = 2
        except:
            k[i] =1

    for i in range(num):
        if k[i] == 2:
            array[i][0], array[i][1] = error_round(array[i][0], array[i][1])

    table = Texttable()
    table.header(header)
    table.set_cols_align(align)
    table.set_cols_dtype(['t']*num)
    for i in range(length):
        list = [0]*num
        for l,m in enumerate(k):
            if m == 1:
                list[l] = array[l][i]
            elif m == 2:
                list[l] = '$' + array[l][0][i] + '\\pm' + array[l][1][i] + '$'
        table.add_row(list)

    if latex == True:
        print(draw_latex(table))
    else:
        print(table.draw())

def write_csv(values, header='',name='data'):
    import csv 
    
    column = len(values)

    try:
        rows = np.shape(values)[1]
    except:
        rows = len(values)


    name = name + '.csv'

    with open(name,'w',newline='') as csvfile:

        writer = csv.writer(csvfile,delimiter=',')

        # Mache erste Zeile mit bezeichnungen
        if header =='':
            firstrow = np.asarray(range(column))+1
        else:
            firstrow = header
        writer.writerow(firstrow)

        for row in range(rows):
        
            list = [0]*column

            for col in range(column):
                list[col] = values[col][row]

            writer.writerow(list)

    
    print('Datei "'+name+'" wurde gespeichert')

# passe die Nachkommastellen in einem array an
def round_align(list):
    n = 0    # die Anzahl der Arrays
    num = 0  # Anzahl der Elemnte pro Array
    try:
        num = np.shape(list)[1]
        n = np.shape(list)[0]
    except:
        n = 1
        num = np.shape(list)[0]
        list = [list]
        
    list_sci = [0]*n
    for i in range(n):
        dummy = [0]*num
        last = 100                  # Anzahl der wenigsten nachkommastellen im Array
        for j in range(num):
            dummy[j] = np.format_float_positional(list[i][j])          
            this = dummy[j]
            k = len(this) 
            decimals = 0                                   

            while this[k-1] != '.':
                decimals += 1
                k -= 1

            if last > decimals:
                last = decimals
        numformat = '{:.'+str(last)+'f}'

        for j in range(num):
            dummy[j] = numformat.format(list[i][j])
        list_sci[i] = dummy
        
    if n == 1:
        return list_sci[0]
    else:
        return list_sci
        