from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Domain, Mapping, Base


def main():

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)

    session = DBSession()

    new_domain = Domain(name='host')
    new_device = Device(bdf='0000:15.1', domain=new_domain)
    new_mapping = Mapping(  iova='0x40800000',
                             phys_addr='0x00000003d4800000',
                             size=2048,
                             device=new_device)
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)

    new_device = Device(bdf='0000:14.1', domain=new_domain)
    new_mapping = Mapping(  iova='0x40900000',
                             phys_addr='0x00000003d4c00000',
                             size=2048,
                             device=new_device)
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)

    new_mapping = Mapping(  iova='0x40d00000',
                             phys_addr='0x00000003d8d00000',
                             size=2048,
                             device=new_device)
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)


    new_device = Device(bdf='0000:16.1', domain=new_domain, name = 'SATA controller: Intel Corporation 82801HM/HEM (ICH8M/ICH8M-E) SATA Controller [AHCI mode] (rev 02)')
    new_mapping = Mapping(  iova='0x40e00000',
                             phys_addr='0x00000003d8d00001',
                             size=2048,
                             device=new_device)
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)


    new_mapping = Mapping(  iova='0x40f00000',
                             phys_addr='0x00000003d9f00000',
                             size=2048,
                             device=new_device)
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)

    session.commit()


if __name__ == '__main__':
    main()
