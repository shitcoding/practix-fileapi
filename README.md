# Practix: Movies Portal + S3 Minio Fileapi
---
## Starting
```
git clone https://github.com/shitcoding/practix-fileapi && cd practix-fileapi
docker compose up --build

# Or to start the app in dev/debug mode:
docker compose -f dc-debug.yml up --build
```

### Loading test data
To load test data to movies database postgres, use:
```
make load_data
```

---
## Tests
To run the tests, use:
```
make test-fastapi
```
