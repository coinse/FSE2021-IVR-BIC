docker kill bic && docker rm bic
docker build --tag dfj-bic:latest .
docker run -dt --name bic -v $(pwd)/resources/workspace:/root/workspace dfj-bic:latest
docker exec -it bic bash
