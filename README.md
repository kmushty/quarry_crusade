# Quarry Crusade

This repository is part of the Quarry Crusade project, designed for efficient management and routing of mining trucks. It leverages Streamlit for a graphical user interface and RTI Connext DDS for communication with mining assets.

## Overview

Quarry Crusade is intended as a solution for managing mining operations, focusing on asset management, truck routing and traffic management (future implementation).

## Key Features

- **Streamlit Interface**: Provides an interactive and intuitive UI for real-time monitoring and control of mining assets (Trucks).
- **DDS Communication**: Utilizes RTI Connext DDS for reliable data exchange with mining trucks, ensuring seamless communication and data integrity. The idea is to integrate with the on-board Mission Manager Embedded software.

## Setup Instructions

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install and Setup RTI Connext DDS**:
   - Download the RTI Connext DDS SDK from [RTI Connext DDS](https://www.rti.com/free-trial?utm_source=google&utm_medium=cpc&utm_campaign=performance_max&utm_term=dynamic_terms&utm_content=autonomous_systems&utm_term=&utm_campaign=cJ+%7C+Leads+%7C+Performance+Max+%7C+USA+%7C+Max.+Conversion&utm_source=adwords&utm_medium=ppc&hsa_acc=4872307840&hsa_cam=20350549833&hsa_grp=&hsa_ad=&hsa_src=x&hsa_tgt=&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=CjwKCAiAhP67BhAVEiwA2E_9g3twtsumIC8ls8AUjbodUj2Qi07AaHO9ozTpVSQp00PA2IIDWhhbGBoCnOMQAvD_BwE)
   - Follow the instructions to install and setup the SDK.

3. **Configure Environment**:
   Ensure RTI Connext DDS is properly configured. Run the setup script:
   ```bash
   source /opt/rti_connext_dds-6.0.1/resource/scripts/rtisetenv_x64Linux3gcc4.8.2.bash
   ```

3. **Launch the Application**:
   Start the Streamlit app to access the graphical interface:
   ```bash
   streamlit run main.py
   ```

## Application Structure

- **Streamlit UI**: 
  - Provides a dashboard for visualizing truck routes and generating new routes.

- **DDS Communication**:
  - Handles data exchange with mining trucks using DDS.

QuarryCrusade/

├── app/

│ ├── dds/

│ │ ├── base/

│ │ │ ├── init.py

│ │ │ ├── handler.py

│ │ │ ├── publisher.py

│ │ │ └── subscriber.py

│ │ ├── idl/

│ │ │ ├── *Contains all IDL Files*

│ │ │ └── USER_QOS_PROFILES.xml

│ │ ├── publishers/

│ │ │ └── QC_publisherList.txt

│ │ ├── subscribers/

│ │ │ ├── QC_subscriberList.txt

│ │ │ └── hxgn_event.py

│ │ ├── init.py

│ │ └── USER_QOS_PROFILES.xml

│ ├── init.py

│ └── main.py

│

├── requirements.txt

├── README.md

└── .env

- `app/`: Contains the Streamlit application.
- `dds/`: Contains the DDS configuration files.
- `idl/`: Contains the IDL files for the DDS topics.
- `requirements.txt`: Contains the Python dependencies.
- `main.py`: The main entry point for the Streamlit application.

## Use Case

Quarry Crusade is tailored for mining operations, providing tools for:
- **Asset Management**: Track and manage mining equipment.
- **Routing**: Optimize routes for mining trucks

## Future Work

- **Traffic Management**: Manage traffic flow and optimize truck movements. This is mostly used for specific traffic zones and refueling/service stations.
- **Asset Management**: Track and manage mining equipment. Add a UI for each mining asset that can be used to view the status of the asset.

## Configuration

- **QoS Profiles**: Defined in XML files to manage communication settings.
- **Topics**: Configured in `topics.yaml` to map messages to DDS topics.
- **IDL Files**: Defined in `idl` folder to map messages to DDS topics.

## Current issues
- The DDS communication is not working as expected. The data is not being sent or received correctly. There is an issue with the XML DDS configuration file.