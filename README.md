This repo contains the a inventory management microservice architecture. 

There are 4 services - products service, inventory service, supplier service and Rabbit-MQ notifications service. The microservices publishes messages to rabbitmq which is consumed by the notifications service.
