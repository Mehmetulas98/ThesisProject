import msvcrt


def keyboardinput():
    global HIZ
    while True:

        if msvcrt.kbhit():
            k = msvcrt.getch()
            esc = str(k)
            k = k.decode("utf-8")

            if(esc != str(b'\x1b')):

                if(k == '1' or k == '2' or k == '3'):
                    HIZ = k
                else:
                    return("Hareket : " + k + " , Hız : " + str(HIZ))
            else:
                break


if __name__ == '__main__':
    while 1:
        result = keyboardinput()
        print(result)
        if(result == None):
            break
