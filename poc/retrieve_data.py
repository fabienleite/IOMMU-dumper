from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Mapping, Base


# List containing devices mappings (global variable to be accessible from outside)
mapping_addresses = []


def create_session():
    """ Creates a session to retrieved data from iommu.db.
    Returns the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


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

    global mapping_addresses

    # Dictionnary to remember devices already added in mapping_addresses
    devices = {}
    # Indoce of the device dictionnary in mapping_addresses
    dict_indice = 0

    # Retrieves all mappings
    for mapping in session.query(Mapping).all():

        data = mapping.__dict__
        device_mapping = {}

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
            # If it's in the list, modify mapping_addresses entry by adding only
            # new values of iova and physical addresses
            if device_name in devices:

                indice_in_dict = devices[device_name]

                if iova not in mapping_addresses[indice_in_dict]["iova"]:
                    mapping_addresses[indice_in_dict]["iova"].append(iova)

                if phys_addr not in mapping_addresses[indice_in_dict]["physical_address"]:
                    mapping_addresses[indice_in_dict]["physical_address"].append(phys_addr)

            # If it's not in the list, add a new entry in mapping_addresses
            else :

                device_mapping["iova"] = [iova]
                device_mapping["physical_address"] = [phys_addr]
                device_mapping["bdf"] = device_name

                # Adding mapping to the list
                mapping_addresses.append(device_mapping)
                devices[device_name] = dict_indice
                dict_indice += 1


if __name__ == '__main__':
    main()
