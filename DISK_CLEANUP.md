# Disk cleanup report (macOS)

## Background
Disk was near full; goal was to free space safely (Docker + common caches + CoreSimulator caches).

## Commands executed
### Docker cleanup
- `docker system prune -f`
- `docker builder prune -f`
- `docker image prune -f`

### User caches cleanup
- `rm -rf ~/Library/Caches/Google/Chrome/*`
- `rm -rf ~/Library/Caches/Homebrew/downloads/*`
- `rm -rf ~/Library/Caches/ms-playwright-go/*`
- `rm -rf ~/Library/Caches/vscode-cpptools/*`

### CoreSimulator cache cleanup
- `rm -rf ~/Library/Developer/CoreSimulator/Devices/*/data/Containers/Data/*`
- `rm -rf ~/Library/Developer/CoreSimulator/Devices/*/data/Containers/Data/Application/*/Library/Caches/*`

## Results
- Verified Docker is working:
  - `docker version` shows Docker Desktop server.
- Verified disk capacity afterwards with:
  - `df -h`

## Notes / Warnings
- Cleaning CoreSimulator and app caches may cause simulator data to be regenerated later.
- Docker prune removes unused images/layers/build cache; it should not delete running containers.
