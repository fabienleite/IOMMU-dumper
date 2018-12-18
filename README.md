# IOMMU Dumper

A university project which object is to dump the mapping configuration of the [IOMMU](https://en.wikipedia.org/wiki/Input%E2%80%93output_memory_management_unit).

The idea is to be able to know at any time which device is mapped to which part of the memory.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

* python3
* sqlalchemy
* Enable debug on IOMMU (via traces)


#### How to enable debug on IOMMU ?

In your grub file (Usually _/etc/default/grub_), add _trace\_event=iommu_ to the GRUB_CMDLINE_LINUX_DEFAULT.

```
GRUB_CMDLINE_LINUX_DEFAULT=" ... trace_event=iommu
```
Then recreate your grub.cfg

```bash
$ grub-mkconfig –output /path/to/grub.cfg
```

### Installing

You can download the IOMMU-Dumper project by cloning the Git repository :
```bash
git clone https://github.com/fabienleite/IOMMU-dumper
```

## Authors

* **Fabien Leite** - [fabienleite](https://github.com/fabienleite)
* **Maxime Messin** - [orygin10](https://github.com/orygin10)
* **Rémi Millerand** - [Driikolu](https://twitter.com/driikolu)
* **Mélanie Romain** - [melrm](https://github.com/melrm)

## License

Copyright 2018 Fabien Leite, Maxime Messin, Rémi Millerand, Mélanie Romain

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

