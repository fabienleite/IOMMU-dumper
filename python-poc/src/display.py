"""
En example of the display we expect to have. Devices are set staticaly with statical adresses, etc.
"""

addresses = [
    {
        "bdf": "0001:00.0",
        "iova": ["0x40000000"],
        "physical_address": ["0x00000003d4c00000", "0x00000003d4800000"],
    },
    {
        "bdf": "0000:14.0",
        "iova": ["0x40800000"],
        "physical_address": ["0x00000003d4400000"],
    },
    {
        "bdf": "0000:15.1",
        "iova": ["0x40c00000"],
        "physical_address": ["0x00000003d4000000"],
    },
    {
        "bdf": "0003:00.0",
        "iova": ["0x44000000"],
        "physical_address": ["0x00000003d0c00000", "0x00000003d0800000"],
    },
]

beginning_and_end = "-" * 54
first_line = " Device | BDF       | VA         | PA"

print(beginning_and_end + "\n" + first_line + "\n" + beginning_and_end)

cnt = 0

for addr in addresses:
    cnt += 1
    biggest_len = (
        len(addr["iova"])
        if len(addr["iova"]) > len(addr["physical_address"])
        else len(addr["physical_address"])
    )
    biggest_len_is_virt = (
        True if len(addr["iova"]) > len(addr["physical_address"]) else False
    )

    for i in range(0, biggest_len):
        beginning = " " + str(cnt) + "      | " + addr["bdf"] + " | "
        if i > 0:
            beginning = " _      | " + "_         | "

        try:
            print(beginning + addr["iova"][i] + " | " + addr["physical_address"][i])
        except IndexError:
            if biggest_len_is_virt:
                print(beginning + addr["iova"] + " | " + "_         ")
            else:
                print(beginning + "_         " + " | " + addr["physical_address"][i])

    print(beginning_and_end)
