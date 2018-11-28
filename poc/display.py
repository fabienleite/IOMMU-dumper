from retrieve_data import main, mapping_addresses

# Calling main() from retrieve_data.py to get data
main()
# In retrieve_data.py, mapping list is in mapping_addresses
addresses = mapping_addresses


# Defining header and separators
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
