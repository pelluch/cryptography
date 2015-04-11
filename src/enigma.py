#!/bin/env python3

import sys

args = sys.argv
disk_files = args[1:4]
patch_file = args[4]
rotors = []
reversed_rotors = []

rotor_counts = [0, 0, 0]
def map_number(num):
    if(num <= 0):
        num += 26
    elif num > 26:
        num -= 26
    return num

def increase_counters(counters, idx = 0):
    counters[idx] += 1
    if(counters[idx] == 26):
        counters[idx] = 0
        if(idx < 2):
            increase_counters(counters, idx + 1)

for path in disk_files:
    rotor = {}
    reversed_rotor = {}

    f = open(path, 'r')
    lines = f.read().splitlines()
    for i, line in enumerate(lines, start = 1):
        rotor[i] = int(line) 
        reversed_rotor[int(line)] = i

    rotors.append(rotor)
    reversed_rotors.append(reversed_rotor)
    f.close()

patch_panel = {}
f = open(patch_file, 'r')
lines = f.read().splitlines()
for line in lines:
    nums = line.split(',')
    patch_input = int(nums[0])
    patch_output = int(nums[1])
    patch_panel[patch_input] = patch_output
    patch_panel[patch_output] = patch_input
f.close()

f = open('../data/reflector2.txt')
reflector = {}
lines = f.read().splitlines()
for i, line in enumerate(lines, start = 1):
    num = int(line)
    reflector[i] = num
    reflector[num] = i

f.close()


plain_text = input("plaintext> ").replace(" ", "").lower()


encrypted_text = ""
for char in plain_text:
    increase_counters(rotor_counts)

    num = ord(char) - 96
    if num in patch_panel:
        num = patch_panel[num]


    # print('Number is', num)
    first_transform = rotors[0][map_number(num + rotor_counts[0])]
    # print('After first rotor:', first_transform, chr(first_transform + 96))

    second_transform = rotors[1][map_number(first_transform + rotor_counts[1] - rotor_counts[0])]
    # print('After second rotor: ', second_transform, chr(second_transform + 96))

    third_transform = rotors[2][map_number(second_transform + rotor_counts[2] - rotor_counts[1])]
    # print('After third rotor: ', third_transform, chr(third_transform + 96))

    mirrored = reflector[third_transform - rotor_counts[2]]
    # print('After reflector: ', mirrored, chr(mirrored + 96))

    fourth_transform = reversed_rotors[2][map_number(mirrored + rotor_counts[2])]
    # print('After third rotor: ', fourth_transform, chr(fourth_transform + 96))

    fifth_transform = reversed_rotors[1][map_number(fourth_transform + rotor_counts[1] - rotor_counts[2])]
    # print('After middle rotor: ', fifth_transform, chr(fifth_transform + 96))

    encrypted = reversed_rotors[0][map_number(fifth_transform + rotor_counts[0] - rotor_counts[1])]
    # print('Reversed final letter: ', encrypted)

    # print(fifth_transform + rotor_counts[0] - rotor_counts[1])
    final_number = map_number(encrypted - rotor_counts[0])
    if final_number in patch_panel:
        final_number = patch_panel[final_number]

    # print('Encrypted char: ', final_number, chr(final_number + 96))
    encrypted_text += chr(final_number + 96)
    # print(third_transform)
    # print(mirrored)
    # print(fourth_transform)
    # print(fifth_transform)
    # print(encrypted)


print("ciphertext>", encrypted_text)