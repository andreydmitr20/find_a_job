docker rm -f python_find_a_job
docker run -t -d --name python_find_a_job -v ~/.PYTHON/find_a_job/:/opt/find_a_job/ -i python_find_a_job:lts
docker ps -aq
