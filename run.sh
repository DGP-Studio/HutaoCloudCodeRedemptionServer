# Docker Image Settings
imageName=homa-code-system
containerName=Homa-Code-System
imageVersion=1.0
ExternalPort=3016
InternalPort=8000

docker build -f Dockerfile -t $imageName:$imageVersion .
docker run -d -itp $ExternalPort:$InternalPort \
    --restart=always \
    --name="$containerName-$imageVersion" \
    --mount type=bind,source="$(pwd)"/generated_codes,target=/code/generated_codes \
    $imageName:$imageVersion