# Kubernetes POC (Manifests + Tilt Demo)

This folder contains a hands-on Kubernetes POC covering core primitives (Pod/Deployment/Service), ConfigMap/Secret usage patterns, the sidecar pattern, and a Tilt-based local dev loop.

## What’s included

### 1) NGINX Deployment + Service
- **Deployment**: 2 replicas of `nginx:latest`.
  - File: [deployment.yaml](deployment.yaml)
- **Service**: `NodePort` service exposing port 80.
  - File: [service.yaml](service.yaml)

Run:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
```

Screenshot space:

```md
<!-- TODO: screenshots for nginx deploy/service -->
![kubectl get pods](../docs/screenshots/k8s-get-pods.png)
![kubectl get svc](../docs/screenshots/k8s-get-svc.png)
```

---

### 2) ConfigMap (Mount NGINX config)
This demo mounts a ConfigMap into `/etc/nginx/conf.d` to serve a custom response.

- ConfigMap with `custom.conf`:
  - File: [nginx-config.yaml](nginx-config.yaml)
- Pod that mounts the config:
  - File: [nginx-config-pod.yaml](nginx-config-pod.yaml)

Run:

```bash
kubectl apply -f nginx-config.yaml
kubectl apply -f nginx-config-pod.yaml
kubectl get pod nginx-configmap-pod
kubectl port-forward pod/nginx-configmap-pod 8081:80
```

Then open: `http://localhost:8081`

Screenshot space:

```md
<!-- TODO: screenshots for nginx configmap mount -->
![ConfigMap](../docs/screenshots/k8s-nginx-configmap.png)
![Port-forward test](../docs/screenshots/k8s-nginx-configmap-test.png)
```

---

### 3) ConfigMap env var demo (references `app-config`)
The pod in [pod-configmap.yaml](pod-configmap.yaml) references a ConfigMap named `app-config` via env vars.

Note: this folder currently contains the **pod** that consumes `app-config`, but not a manifest defining the `app-config` ConfigMap.

Create it (example):

```bash
kubectl create configmap app-config \
  --from-literal=APP_NAME=myapp \
  --from-literal=APP_ENV=dev

kubectl apply -f pod-configmap.yaml
kubectl exec -it configmap-demo -- env | egrep 'APP_NAME|APP_ENV'
```

Screenshot space:

```md
<!-- TODO: screenshots for env-from-configmap -->
![ConfigMap env vars](../docs/screenshots/k8s-configmap-env.png)
```

---

### 4) Secret env var demo (references `db-secret`)
The pod in [pod-secret.yaml](pod-secret.yaml) references a Secret named `db-secret` via env vars.

Note: this folder currently contains the **pod** that consumes `db-secret`, but not a manifest defining the `db-secret` Secret.

Create it (example):

```bash
kubectl create secret generic db-secret \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASS='pass123'

kubectl apply -f pod-secret.yaml
kubectl exec -it secret-demo -- env | egrep 'DB_USER|DB_PASS'
```

Screenshot space:

```md
<!-- TODO: screenshots for env-from-secret -->
![Secret env vars](../docs/screenshots/k8s-secret-env.png)
```

---

### 5) Sidecar pattern demo (shared logs)
A single Pod with:
- **app container** writing logs to `/var/log/app.log`
- **sidecar container** tailing the same file
- shared volume: `emptyDir` mounted into both containers

File: [sidecar.yaml](sidecar.yaml) (same as [sidecar-demo.yaml](sidecar-demo.yaml))

Run:

```bash
kubectl apply -f sidecar.yaml
kubectl logs -f sidecar-demo -c sidecar
```

Screenshot space:

```md
<!-- TODO: screenshots for sidecar demo -->
![Sidecar logs](../docs/screenshots/k8s-sidecar-logs.png)
```

---

## Tilt demo (local dev loop)
The Tilt demo builds a tiny NGINX image serving a local `index.html`, deploys it to Kubernetes, and port-forwards it.

Files:
- Tilt config: [tilt-demo/Tiltfile](tilt-demo/Tiltfile)
- K8s manifests: [tilt-demo/k8s.yaml](tilt-demo/k8s.yaml)
- Image build: [tilt-demo/Dockerfile](tilt-demo/Dockerfile)
- Web content: [tilt-demo/index.html](tilt-demo/index.html)

Run:

```bash
cd tilt-demo

tilt up
```

Then open the forwarded URL shown by Tilt (configured as `port_forwards=8080`).

Screenshot space:

```md
<!-- TODO: screenshots for tilt demo -->
![Tilt UI](../docs/screenshots/tilt-ui.png)
![Tilt demo page](../docs/screenshots/tilt-demo-page.png)
```
