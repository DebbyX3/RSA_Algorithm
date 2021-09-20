'''
RSA
Questa versione di RSA riesce a generare chiavi a circa 1096 bit, partendo da numeri primi da 2^500 fino a 2^550. 

Il minimo indispensabile al giorno d'oggi è usare chiavi a 1024 bit (meglio a 2048)
'''

import math
import sympy
import random
import textwrap

from decimal import Decimal, localcontext

# ------------------ CONSTANTS
INIT_RANGE_PRIME = 2**500
END_RANGE_PRIME = 2**550

# ------------------ FUNCTIONS DEF
'''
Nota: questa funzione non è stata usata visto che la funz math.pow(a, b, mod) 
è molto più efficente quando si trattano numeri in modulo. La tengo per reference.
'''
def expBySquaring(x, n):
    if n == 1:
        return x
    elif n%2 == 0: #n is even        
        return expBySquaring(x * x, n/2)
    elif n > 2 and n%2 == 1: #n is odd
        return x * expBySquaring(x * x, (n-1)/2)

# ------------------ BEGIN RSA 
def main():
    # Select p, q, where p != q, both prime
    p = sympy.randprime(INIT_RANGE_PRIME, END_RANGE_PRIME)

    # Loop until 'p' and 'q' are not equals (when using huge numbers it is almost never the case)
    while (q := sympy.randprime(INIT_RANGE_PRIME, END_RANGE_PRIME)) == p:
        pass

    print("Prime numbers: \np =  {0} \nq = {1}".format(p, q))

    # Calculate n = p*q
    n = p*q
    print("\nn = (p*q) = {0}".format(n))

    # Calculate phi(n) = (p-1)*(q-1)
    phi = (p-1)*(q-1)
    print("\nphi = (p-1)*(q-1) = {0}".format(phi))

    # Select an integer e such that 1 < e < phi(n) and e is coprime to phi(n) (non hanno divisori in comune), 
    # in other words, gcd(e, phi(n)) = 1

    '''
    Nota: l'esponente 'e' è generalmente fissato sempre a 65537 ((2^16)+1) in RSA, 
    anche quando si usano chiavi molto grandi (tipo a 1024 o 2048 bit)

    Se si segue la generazione indicata formalamente dall'algoritmo, 'e' dovrebbe essere generata così:
    e = random.randint(1+1, phi-1) #per estremi non compresi ho fatto +1 e -1

    Non è importante che 'e' sia sempre lo stesso valore, anche perchè 'e' è di fatto una chiave 
    pubblica e quindi sempre visibile. Inoltre, un esponente molto grande, come quello che uscirebbe 
    generato da un random, rallenterebbe di molto la crittazione del messaggio
    '''
    # Con 'e' random
    # e = random.randint(1+1, phi-1) #per estremi non compresi ho fatto +1 e -1

    # Con 'e' fisso 
    e = (2**16)+1  #65537

    # Check if gcd(e, phi(n)) is 1. If it's not, then re-generate a new 'e'
    while math.gcd(phi, e) != 1:
        e = random.randint(1+1, phi-1)

    print("\ne = {0} \ngcd(phi, e) = {1} (should be 1)".format(e, math.gcd(phi, e)))

    # Calculate d to satisfy the congruence relation:
    # d*e mod phi(n) = 1 mod phi(n)
    '''
    1 mod qualsiasi cosa è sempre = 1, quindi anche d*e mod phi(n) deve essere uguale a 1
    visto che so che, per la proprietà dei resti e del quoziente, d*e = 1 + x * phi(n)
    posso dedurre d = (1 + x * phi(n))/e, per un qualche x, che posso scegliere a mio piacimento! 
    L'importante è che la 'd' calcolata in questo modo sia un intero, quindi ciclo finchè non lo è

    Nota: un'altra versione dell'algoritmo trova 'd' facendo: d=e^(-1) mod phi(n)
    Personalmente, ho visto usare più frequentemente la versione che ho codificato, nella quale cerco x finchè 
    d = (1 + x * phi(n))/e non diventa intero.

    Il downside di questo metodo sta nella precisione della divisione 
    (discorso un po' lungo da scrivere, forse meglio discuterne all'orale?)
    In pratica, se non si hanno a disposizione sufficienti cifre decimali, all'aumentare dei bit della 
    chiave o dei numeri primi utilizzati succede che la divisione d = (1 + x * phi(n))/e non è più corretta.
    Infatti, se il risultato ha molte cifre decimali, python le arrotonda, creando inevitabilmente errori nel
    risultato finale. 
    Nella fattispecie di questo caso, noi vogliamo che d = (1 + x * phi(n))/e sia un intero, in modo da 
    rispettare le proprietà della divisione (d*e = 1 + x * phi(n)).

    Se 'd', dopo la divisione d = (1 + x * phi(n))/e risulta essere 5,00000000...411, allora non deve essere considerato
    come intero, visto che le ultime cifre decimali non sono tutte 0. Se però si utilizzano poche cifre 
    nella rappresentazione decimale, python tronca il numero usando le cfre a disposizione, scrivendo d=5,00000000...000,
    rendendo di fatto 'd' un intero. Questa approssimazione sballa completamente l'algoritmo RSA, rendendolo di fatto sbagliato
    e generando una chiave di decrittazione 'd' errata.

    Per prevenire questo errore, è necessario aumentare lo spazio dedicato alle cifre decimali. Nota bene: se la dimensione della 
    chiave cresce, allora dovrebbero crescere anche le cifre decimali utilizzate per il calcolo di 'd'. Non ho trovato una correlazione
    'matematica' che connette dimensione della chiave e cifre deciamli a disposizione, perciò ho aumentato a 999 le cifre dec. di 'd'.

    Facendo vari test, con numeri primi di partenza 'p' e 'q' che possono arrivare fino 2^200 (200 bit), la chiave 'd' 
    è calcolata correttamente, in particolare, 'd' risulta essere di dimensione circa 400 bit (2^400)

    Con numeri primi 'p' e 'q' che possono arrivare fino 2^550 (550 bit), la chiave 'd' 
    è calcolata ancora correttamente, in particolare, 'd' risulta essere di dimensione circa 1096 bit (2^1096)
    '''
    with localcontext() as ctx:
        ctx.prec = 999

        x = 1
        d = Decimal(1 + x * phi)/Decimal(e)

        while d != d.to_integral_value():
            
            d = Decimal(1 + x * phi)/Decimal(e)
            x = x+1

        d = int(d)

    print("\nd = {0} \nx = {1} \nd*e = 1 + x * phi(n)".format(d, x))

    print("\n------Public keys: \nn = {0} \n\ne = {1}".format(n, e))
    print("\n------Private keys: \np = {0} \n\nq = {1} \n\nd = {2}".format(p, q, d))


#------------------------------------- ENCRYPTION

def RSAEnc(plaintext, e, n):
    '''
    Si spezzetta il messaggio in blocchi più piccoli di 'n', ovvero in blocchi di floor(log_2(n)) bit. 
    Ogni blocco è crittato. Si mandano i blocchetti crittografati e all'arrivo si decrittano e ricompongono

    Quello che faccio qui:
    - prendo il plaintext
    - codifico il plaintext in utf-8 (unicode)
    - codifico il plaintext da utf-8 a esadecimale
    - trasformo la stringa esadecimale in decimale (da base 16 a 10), in modo da poter 
    spezzare il messaggio in blocchi di floor(log_2(n)) bit e in modo da avere un messaggio che posso mandare
    - visto che sono in decimale, i blocchi devono essere di lunghezza floor(log_10(n)), notare il log 10,
    quindi cerco il valore di floor(log_10(n))
    - spezzo in blocchi < n lunghi al max floor(log_10(n)) (siamo nel sistema decimale!) e li metto tutti in una lista
    - critto ogni blocco nella lista
    - mando tutto

    Nota bene: l'intento iniziale era di usare il binario al posto del decimale per poter contare effettivamente i bit di 
    floor(log_2(n)) e spezzare il messaggio in quanti bit mi dice il log2. Purtroppo però, una volta spezzati, 
    bisognava portarli di nuovo in decimale: ma questa trasformazione poteva modificare il messaggio!

    Per esempio: se il msg era '100100001' e si doveva spezzare ogni 6 bit, usciva: ['100100', '001'], che però portando
    in decimale, usciva '36', che si traduceva anche a desinazione in '100100001' correttamente, ma il secondo elemento
    della lista '001' in decimale è 1, che ri-tradotto non ci dà '001', ma solo '1'! E quindi quando si ri-concatena
    il msg a destinazione, questo non sarà più '100100001', ma 1001001', sbagliando di fatto la codifica!

    In decimale questo non accade
    '''

    e = int(e)
    n = int(n)

    plaintextInDec = int(plaintext.encode("utf-8").hex(), 16)

    maxBitBlockInDec = math.floor(math.log(n, 10))
    messageSplitInDec = textwrap.wrap(str(plaintextInDec), maxBitBlockInDec)

    ciphertextToSend = []

    for block in messageSplitInDec:
        ciphertextToSend.append(pow(int(block), int(e), int(n)))

    print("\n----- RSA Encrypter -----")

    print("\nMessage to send: ", plaintext)
    print("\nMessage to encrypt in decimal form: ", plaintextInDec)
    print("\nMessage split in blocks < n: ", messageSplitInDec)
    print("\nCiphertext to send: ", ciphertextToSend)

    return ciphertextToSend

#------------------------------------- DECRYPTION
def RSADec(ciphertext, d, n):
    '''
    Per decrittare, faccio le operazioni inverse del crittaggio

    - Prendo i blocchi ricevuti e li decritto
    - Riattacco i blocchi decifrati in un unico numero
    - Trasformo il numero concatenato da decimale a esadecimale
    - Trasformo l'esadecimale in uft-8, tornando alla stringa di partenza
    '''

    d = int(d)
    n = int(n)
    
    ciphertextDecrypted = []

    for block in ciphertext:
        ciphertextDecrypted.append(pow(block, d, n))

    concatBlocks = int("".join(map(str, ciphertextDecrypted)))

    decryptedMsg = bytes.fromhex(format(concatBlocks, 'x')).decode('utf-8')

    print("\n----- RSA Decrypter -----")

    print("\nMessage received: ", ciphertext)
    print("\nMessage received after decrption: ", ciphertextDecrypted)
    print("\nBlocks concatenated: ", concatBlocks)
    print("\nPlaintext message: ", decryptedMsg)

    return decryptedMsg

if __name__ == "__main__":
    main()