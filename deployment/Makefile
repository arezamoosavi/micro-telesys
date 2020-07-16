start-registery:
	docker-compose -f docker-registery.yml up --build -d

clean-registery:
	docker-compose -f docker-registery.yml down -v

docker-build:
	docker build -t nameko-api .
	docker tag nameko-api 10.10.0.1:5000/nameko-api:v1

docker-run:
	docker run -p 3000:80 --name nameko-api -it --rm 10.10.0.1:5000/nameko-api:v1

docker-push:
	docker push 10.10.0.1:5000/nameko-api:v1

check-registry:
	curl -X GET http://10.10.0.1:5000/v2/nameko-api/tags/list

docker-bash:
	docker run --name nameko-api -it --rm 10.10.0.1:5000/nameko-api:v1 bash

del-minikube:
	minikube delete

init-minikube:
	minikube start --insecure-registry="10.10.0.1:5000"

create-dep:
	kubectl create deployment signapp --image=10.10.0.1:5000/nameko-api:v1 --dry-run=client -o=yaml > k8s/deployment.yaml

deploy-mq-redis:
	kubectl apply -f k8s/rmq-redis/

deploy-app:
	kubectl apply -f k8s/nameko/deployment.yaml

deploy-service:
	kubectl apply -f k8s/nameko/services.yaml

all-deploy:
	kubectl apply -f k8s/rmq-redis/
	kubectl apply -f k8s/nameko/services.yaml
	kubectl apply -f k8s/nameko/deployment.yaml


delete-all-deploy:
	kubectl delete -f k8s/nameko/
	kubectl delete -f k8s/rmq-redis/