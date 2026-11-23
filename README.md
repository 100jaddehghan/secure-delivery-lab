# Secure Delivery Lab

A FastAPI health service with a GitHub Actions pipeline that tests code, audits Python dependencies, scans a container, and publishes the verified image.

| Stage | Check |
| --- | --- |
| Test | Assert that the health endpoint returns HTTP 200 and the expected payload |
| Audit | Fail if pip-audit finds known vulnerabilities in the pinned runtime dependencies |
| Build and smoke-test | Run the image as UID 10001 with a read-only filesystem and check its HTTP endpoint |
| Scan | Block fixable high and critical image vulnerabilities using Trivy |
| Publish | Push the same tested image to GHCR on a successful main-branch run |

## Run locally

```sh
docker build -t secure-delivery-lab .
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges -p 127.0.0.1:8000:8000 secure-delivery-lab
```

In another terminal, request `http://127.0.0.1:8000/healthz`. The JSON response is `{"status":"ok"}`.

## Demonstrate a blocked release

Open a pull request that changes the health payload while keeping the test as written. The test will fail, and there is no publish job for pull requests. Close the PR or restore the expected payload. A successful run on `main` publishes an image tagged `sha-<commit>`.

## Roll back

Before replacing a running container, record its image digest from the registry. If the new version fails, remove the failed container and recreate it using the previous digest.

```sh
docker rm -f secure-delivery-lab
docker run -d --name secure-delivery-lab --read-only --cap-drop ALL \
  --security-opt no-new-privileges -p 127.0.0.1:8000:8000 \
  ghcr.io/100jaddehghan/secure-delivery-lab@sha256:<previous-digest>
curl --fail http://127.0.0.1:8000/healthz
```

Wait for the container to become healthy if the first request arrives during startup. This repository publishes a container image. Deployment to a host is manual.
