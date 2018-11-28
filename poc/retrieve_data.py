from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Mapping, Base


# List containing devices mappings (global variable to be accessible from outside)
mapping_addresses = []


def create_session():
    """ Create a session to retrieved data from iommu.db.
    Return the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def adding_in_mapping_list(device, iova, phys_addr):
    """ Add an entry to the mapping list mapping_addresses.
    Param :
        - device : the bdf of the device
        - iova : the virtual address of the mapping
        - phys_addr : the physical address of the mapping"""

    global mapping_addresses
    device_mapping = {}

    device_mapping["iova"] = [iova]
    device_mapping["physical_address"] = [phys_addr]
    device_mapping["bdf"] = device

    # Adding mapping to the list
    mapping_addresses.append(device_mapping)

def updating_mapping_list(indice, iova, phys_addr):
    """ Update an entry in the mapping list mapping_addresses.
    Add only new values of iova and physical addresses.
    Param :
        - indice : the indice of the dictionnary in the list
        - iova : the virtual address to be added
        - phys_addr : the physical address to be added"""

    global mapping_addresses

    if iova not in mapping_addresses[indice]["iova"]:
        mapping_addresses[indice]["iova"].append(iova)

    if phys_addr not in mapping_addresses[indice]["physical_address"]:
        mapping_addresses[indice]["physical_address"].append(phys_addr)


def main():
    """ Retrieve data from iommu.db and format them into a list of dictionnaries
    named mapping_addresses.
    The format of the list is like the following:
    mapping_addresses = [
        {
            "bdf": "0000:14.0",
            "iova": ["0x40800000"],
            "physical_address": ["0x00000003d4400000"],
        },
        ...
        {
            "bdf": "0001:00.0",
            "iova": ["0x40000000", "0x40000008"],
            "physical_address": ["0x00000003d4c00000", "0x00000003d4800000"],
        }
    ] """

    session = create_session()

    # Dictionnary to remember devices already added in mapping_addresses
    devices = {}
    # Indoce of the device dictionnary in mapping_addresses
    dict_indice = 0

    # Retrieves all mappings
    for mapping in session.query(Mapping).all():

        data = mapping.__dict__
        try:
            # Retrieves the device corresponding to the device id in the mapping
            device = session.query(Device).filter_by(id = int(data["devices_id"])).one()
            device_name = str(device.name)
        except Exception as e:
            raise
        else:

            iova = str(data["iova"])
            phys_addr = str(data["phys_addr"])

            # Before adding the mapping, check if device isn't already in the list
            # If it's in the list, update mapping list
            if device_name in devices:

                indice_in_dict = devices[device_name]
                updating_mapping_list(indice_in_dict, iova, phys_addr)

            # If it's not in the list, add a new entry in mapping_addresses
            else :

                adding_in_mapping_list(device_name, iova, phys_addr)
                devices[device_name] = dict_indice
                dict_indice += 1


if __name__ == '__main__':
    main()
