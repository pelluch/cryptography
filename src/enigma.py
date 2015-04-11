#!/bin/env python3

import sys

args = sys.argv
disk_files = args[1:4]
patch_file = args[4]
rotors = []
reversed_rotors = []

rotor_counts = [0, 0, 0]

# Handles cases when disks make a full turn
def map_number(num):
    if(num <= 0):
        num += 26
    elif num > 26:
        num -= 26
    return num

# "Turns" the disks in odometer style
def increase_counters(counters, idx = 0):
    counters[idx] += 1
    if(counters[idx] == 26):
        counters[idx] = 0
        if(idx < 2):
            increase_counters(counters, idx + 1)

# Read disk files
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

# Read patch panel
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

# Read reflector file
reflector_array = [
    15,
    18,
    14,
    26,
    24,
    16,
    25,
    21,
    17,
    23,
    20,
    22,
    19
]

# reflector_array = [
#     25,
#     18,
#     21,
#     8,
#     17,
#     19,
#     12,
#     4,
#     16,
#     24,
#     14,
#     7,
#     15,
#     11,
#     13,
#     9,
#     5,
#     2,
#     6,
#     26,
#     3,
#     23,
#     22,
#     10,
#     1,
#     20
# ]

# Make hash with reflector for ease of use
reflector = {}
for i, reflection in enumerate(reflector_array, start = 1):
    reflector[i] = reflection
    reflector[reflection] = i

# Get user input, remove spaces and transform to lower case
plain_text = input("plaintext> ").replace(" ", "").lower()
used_input = ""

encrypted_text = ""
for char in plain_text:
    increase_counters(rotor_counts)

    num = ord(char) - 96
    # Ignore invalid characters
    if(num < 1 or num > 26):
        continue

    used_input += char

    # Apply patch panel
    if num in patch_panel:
        num = patch_panel[num]

    first_transform = rotors[0][map_number(num + rotor_counts[0])]
    second_transform = rotors[1][map_number(first_transform + rotor_counts[1] - rotor_counts[0])]
    third_transform = rotors[2][map_number(second_transform + rotor_counts[2] - rotor_counts[1])]

    mirrored = reflector[third_transform - rotor_counts[2]]

    fourth_transform = reversed_rotors[2][map_number(mirrored + rotor_counts[2])]
    fifth_transform = reversed_rotors[1][map_number(fourth_transform + rotor_counts[1] - rotor_counts[2])]
    encrypted = reversed_rotors[0][map_number(fifth_transform + rotor_counts[0] - rotor_counts[1])]

    # Align with panel
    final_number = map_number(encrypted - rotor_counts[0])
    if final_number in patch_panel:
        final_number = patch_panel[final_number]

    encrypted_text += chr(final_number + 96)
    # print(encrypted)


print("ciphertext>", encrypted_text)