import os
import re
import pandas as pd
from past.builtins import raw_input
import sys
import traceback


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit


def get_rotor(abc, key):
    array = []
    for _ in abc:
        array += [[_, key[abc.index(_)]]]
    return array


def rotors_positions(pos_1, pos_2, pos_3, a1, a2, a3):
    for i in range(pos_1 - 1):
        a1 = a1[1:27] + a1[0]
    for i in range(pos_2 - 1):
        a2 = a2[1:27] + a2[0]
    for i in range(pos_3 - 1):
        a3 = a3[1:27] + a3[0]


def rotors(letter, a1, a2, a3, key_1, key_2, key_3, refl):
    r_1 = get_rotor(a1, key_1)
    r_2 = get_rotor(a2, key_2)
    r_3 = get_rotor(a3, key_3)
    r_4 = get_rotor(abc, refl)

    array_rotor_1 = pd.DataFrame(data=r_1).rename(columns={0: "input", 1: "output"})
    array_rotor_2 = pd.DataFrame(data=r_2).rename(columns={0: "input", 1: "output"})
    array_rotor_3 = pd.DataFrame(data=r_3).rename(columns={0: "input", 1: "output"})
    array_refl = pd.DataFrame(data=r_4).rename(columns={0: "input", 1: "output"})

    output_1 = pd.Series(array_rotor_1.query('input in @letter')['output'], dtype='string').str.cat()
    output_2 = pd.Series(array_rotor_2.query('input in @output_1')['output'], dtype='string').str.cat()
    output_3 = pd.Series(array_rotor_3.query('input in @output_2')['output'], dtype='string').str.cat()
    output_r = pd.Series(array_refl.query('input in @output_3')['output'], dtype='string').str.cat()
    output_4 = pd.Series(array_rotor_3.query('output in @output_r')['input'], dtype='string').str.cat()
    output_5 = pd.Series(array_rotor_2.query('output in @output_4')['input'], dtype='string').str.cat()
    output_6 = pd.Series(array_rotor_1.query('output in @output_5')['input'], dtype='string').str.cat()

    return output_6


def rotating(a1, a2, a3, bp1, bp2):
    a11 = a1
    a21 = a2
    a31 = a3
    a11 = a1[1:26] + a1[0]

    if a11[0] in bp1:
        a21 = a2[1:26] + a2[0]
        if a21[0] in bp2:
            a31 = a3[1:26] + a3[0]
    return a11, a21, a31


def plug_change(str):
    str_2 = str[1] + str[0]
    for i in abc:
        if str == f"{i}{i}":
            return
    try:
        if plugboard[str] == False:
            plugboard[str] = True
            str1=str
        else:
            plugboard[str] = False
            str1=str
    except:
        if plugboard[str_2] == False:
            plugboard[str_2] = True
            str1=str_2
        else:
            plugboard[str_2] = False
            str1 = str_2
    letter_1 = str1[0]
    letter_2 = str1[1]
    for element in plugboard.keys():
        if element in str1:
         continue
        if (letter_1 in element) or (letter_2 in element):
         if plugboard[element]==True:
          plugboard[element] = False


def plug_usage(letter):
    for i in abc:
        if letter in i:
            continue
        try:
            if (plugboard[f"{letter}{i}"] == True):
                return i
            else:
                continue
        except:
            if (plugboard[f"{i}{letter}"] == True):
                return i
            else:
                continue

    return letter


# ------------------------------------------------------------------------------------------------------------------
while True:
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    abc_1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    abc_2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    abc_3 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    abc_4 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    abc_5 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()

    reflector_b = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower()
    reflector_c = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'.lower()

    key_11 = 'ekmflgdqvzntowyhxuspaibrcj'.lower()
    key_21 = 'ajdksiruxblhwtmcqgznpyfvoe'.lower()
    key_31 = 'bdfhjlcprtxvznyeiwgakmusqo'.lower()
    key_41 = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'.lower()
    key_51 = 'VZBRGITYUPSDNHLXAWMJQOFECK'.lower()



    plugboard = {}
    for i in abc:
        for j in abc:
            if f"{j}{i}" in plugboard.keys():
                continue
            if i in j:
                continue
            plugboard[f"{i}{j}"] = False

    if os.path.exists('settings.txt'):
        file = open('settings.txt', 'r')
        rotors_str = str(file.readline()).replace('rotors: ', '').replace('\n', '')
        rotors_arra = rotors_str.split(' ')

        positions_str = str(file.readline()).replace('rotors_positions: ', '').replace('\n', '')
        positions = re.sub(' +', ' ', positions_str).split(' ')

        plugboard_str = str(file.readline()).replace('plugboard: ', '').replace('\n', '')
        plugboard_array = re.sub(' +', ' ', plugboard_str).split(' ')
        file.close()
        print('Rotors positions and plugboard are imported')
    else:
        while True:
            rotors_str = str(input("Choose which of 5 rotors and 2 reflectors you want to use:\nrotors: 1, 2, 3, 4, "
                                   "5\nreflector: b, c\nwrite them in order you want to be them in machine: 3 5 1 b\n")).lower()
            rotors_arra = rotors_str.split(' ')

            if len(rotors_str) == 0:
                print("These parameters must be entered.")
                continue

            if (rotors_arra[0] in ['1', '2', '3', '4', '5']) and \
                    (rotors_arra[1] in ['1', '2', '3', '4', '5']) and \
                    (rotors_arra[2] in ['1', '2', '3', '4', '5']) and \
                    (rotors_arra[3] in ['b', 'c']):
                break
            else:
                print('Check your input')

        while True:
            plugboard_str = str(
                input('You can choose two letters of your alphabet and write them as (ab) without brackets.'
                      'You can take several pairs, just so that all letters are different. Write it down in '
                      'format (ab cd) without brackets.\nIf you dont want to use this then press enter\n')).lower()

            if len(plugboard_str) != 0:
                plugboard_str = re.sub(r'[^a-zA-Z ]+', '', plugboard_str)
                plugboard_array = re.sub(' +', ' ', plugboard_str).split(' ')

                flag = False
                for unit in plugboard_array:
                    try:

                        s2 = unit[1] + unit[0]
                    except:
                        print('Check your input')
                        flag = True
                        break
                    if (unit[1] in "с") or (unit[0] in "с"):  # тут русская с
                        print("Check your keyboard layout. You entered Russian с")  # тут русская с
                        flag = True
                    if (s2 not in plugboard.keys()) and (unit not in plugboard.keys()):
                        print(
                            "The connections you specified do not exist. If you think everything was right then check the input format.")
                        flag = True
                if flag == True:
                    continue
                else:
                    break
            else:
                break

        # --------------------------------------------------------------------------------------------------------------------------
        while True:
            positions_str = str(input('Write the starting positions of each of 3 rotors (as (13 23 17) without brackets)'
                                      '(they will be taken modulo the length of the alphabet).\nIf you dont want to '
                                      'use this then press enter\n')).lower()

            if len(positions_str) != 0:
                positions_str = re.sub(r'\D ', '', positions_str)
                positions = re.sub(' +', ' ', positions_str).split(' ')
                if len(positions) != 3:
                    print('Check ypur input')
                    continue
                flag_1 = False
                for unit in positions:
                    try:
                        int(unit)
                    except:
                        print(
                            "Input must be 3 integers with spaces in between. If it is then check the input format")
                        flag_1 = True

                if flag_1 == True:
                    continue
                else:
                    break
            else:
                break



    # -------------------------------------------------------------------------------------------------------------------------

    word = str(input('Write a word or several words to be encrypted (no spaces or punctuation marks): \n')).lower()
    word = re.sub(r'[^a-zA-Z]', '', word)

    for unit in rotors_arra:
        if unit in '1':
            rotors_arra += ['r']
        elif unit in '2':
            rotors_arra += ['f']
        elif unit in '3':
            rotors_arra += ['w']
        elif unit in '4':
            rotors_arra += ['k']
        elif unit in '5':
            rotors_arra += ['a']

    rotors_array = []
    for unit in rotors_arra[0:4]:
        if unit in '1':
            rotors_array += [[abc_1, key_11]]
        elif unit in '2':
            rotors_array += [[abc_2, key_21]]
        elif unit in '3':
            rotors_array += [[abc_3, key_31]]
        elif unit in '4':
            rotors_array += [[abc_4, key_41]]
        elif unit in '5':
            rotors_array += [[abc_5, key_51]]
        elif unit in 'b':
            rotors_array += [[abc, reflector_b]]
        elif unit in 'c':
            rotors_array += [[abc, reflector_c]]

    rotors_array += [rotors_arra[4:7]]

    if len(plugboard_str) != 0:
        for _ in plugboard_array:
            plug_change(_)
    if len(positions_str) != 0:
        rotors_positions(int(positions[0]) % len(abc), int(positions[1]) % len(abc), int(positions[2]) % len(abc),
                         rotors_array[0][0], rotors_array[1][0], rotors_array[2][0])

    letter_array = []
    for _ in word:
        letter_array += [_]

    """plug_change
       input
       plug_usage
       rotors
       rotating
       plug_usage
       output"""

    decoded = []
    print('--------------------------------------------------------------------------------------------------------------------')
    for char in letter_array:
        rotors_array[0][0], rotors_array[1][0], rotors_array[2][0] = rotating(rotors_array[0][0], rotors_array[1][0],
                                                                              rotors_array[2][0], rotors_array[4][0],
                                                                              rotors_array[4][1])
        a = plug_usage(char)

        b = rotors(a, rotors_array[0][0], rotors_array[1][0], rotors_array[2][0],
                   rotors_array[0][1], rotors_array[1][1], rotors_array[2][1], rotors_array[3][1])

        c = plug_usage(b)


        decoded += c
    decoded = ''.join(decoded)
    print(word, '--------', decoded, '------------', positions_str, '-----------', plugboard_str)

    end = str(input('Do you want to save this settings for the next session?\nyes/no\n ')).lower()

    if end in 'yes':
        settings = open('settings.txt', 'w')
        settings.write(f'rotors: {rotors_str}\n'
                       f'rotors_positions: {positions_str}\n'
                       f'plugboard: {plugboard_str}\n')
        settings.close()
    else:
        if os.path.exists('settings.txt'):
            os.remove('settings.txt')
            print('Settings are reset to zero')

    print('If you find an error or something went wrong, please please contact at Telegram: @Cerseq')
    end_1 = str(input('Do you want to run program again? yes/no\n')).lower()
    if end_1 in 'no':
        break

