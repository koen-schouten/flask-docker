
Make docker container have access to docker api:
docker run -t -d --name mypython -v /var/run/docker.sock:/var/run/docker.sock python