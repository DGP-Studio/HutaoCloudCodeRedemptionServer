# Image Settings
imageName=homa-code-system
imageVersion=1.0

docker build --no-cache -f Dockerfile -t $imageName:$imageVersion --target runtime .