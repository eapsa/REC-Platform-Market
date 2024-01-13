<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]
### Disclaimer

This microservice was necessary for me to graduate in the Master's Degree in Engineering of Computer and Telematics. If interested, check [MSC Eduardo Almeida]() to know more!

### REC Platform - Market Microservice

The Renewable Energy Community Platform consists in a microservices API to enable and enhance Peer-to-Peer energy Transactions between Prosumers and consumers of a community.

The market microservice acts as a computing algorithm, by processing all the electricity measurements from the meters microservice at a predefined rate and employing a market algorithm to create energy matches between community members and allocate the remaining energy to the public grid.

Why building a REC Platform using microservices:
* The project was developed together with other devs
* Changes in one particular module forced to shutdown/reboot the whole API.
* This is part of a research program, therefore multiple experimental ideas, frameworks, and scripts were used. 


<p align="right">(<a href="#readme-top">Back to Top</a>)</p>



### Built With

To make the API work, these are the core features of the Market:

* [Python](https://www.python.org/)
* [Docker Container](https://www.docker.com/)
* [gRPC](https://grpc.io/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

The Market microservice requires Meters microservice to be operational.

Other microservices links:
* [Meter microservice](https://github.com/eapsa/REC-Platform-Meters/)
* [Gateway microservice](https://github.com/AnBapDan/REC-Platform-Gateway/)
* [Transactions microservice](https://github.com/AnBapDan/REC-Platform-Transactions/)

### Prerequisites

There is a secure communication between this microservice and the Transactions one, therefore ensure that a '.pem' certificate  is stored in market/secrets.
The Meters microservice requires a MongoDB database to store the data. Update the info on market_config.init.

## Deployment
The all microservices structure is supposed to be deployed using Docker Swarm. Below are the steps to achieve it correctly.

1. Create a network that hosts all the stack
    ```sh
    docker network create --driver=overlay --attachable RECNetwork
    ```


2. Run every Dockerfile to create its image
    ```sh
    docker build -t <img_name>:<version>
    ```

3. Deploy the whole Docker stack
    ```sh
    docker stack deploy -c docker-compose.yml RECNetwork
    ```
For more info check [REC Platform - Gateway](https://github.com/AnBapDan/REC-Platform-Gateway/)

## Contact

Eduardo Almeida - eapsa@ua.pt

Project Link: [https://github.com/eapsa/REC-Platform-Market.git](https://github.com/eapsa/REC-Platform-Market.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/eduardo-almeida-1a20b8257/
