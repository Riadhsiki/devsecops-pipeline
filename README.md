# DevSecOps Pipeline

Projet 5NIDS2 (ESPRIT) realise par **Riadh Tarhouni et Balkis Baraket**, encadre par M. Taoufik Bessrour.

Objectif : securiser un pipeline CI/CD (GitHub Actions) autour d'une application Flask volontairement vulnerable,
avec des controles automatiques qui bloquent toute faille avant la production (demarche DevSecOps, "shift-left").

## Pipeline (`.github/workflows/ci.yml`)

Declenche a chaque push et pull request. Les jobs sont enchaines : **si un job echoue, les suivants sont ignores**.
Le job `notify` s'execute toujours et envoie le resultat sur Discord.

| Stage | Job | Outil | Bloque si |
|---|---|---|---|
| 1 | `build` | Docker | le build echoue |
| 2 | `unit_tests` | pytest | un test echoue |
| 3 | `secrets_scan` | Gitleaks | nouvelle fuite de secret |
| 4 | `sast_bandit` | Bandit | severite MEDIUM ou plus |
| 5 | `scan_dependencies` | Trivy (fs) | CVE CRITICAL/HIGH corrigeable |
| 6 | `iac_scan` | Checkov | un controle echoue |
| 7 | `docker_scan` | Trivy (image) | CVE CRITICAL/HIGH corrigeable |
| 8 | `sbom` | Syft | (livrable, CycloneDX) |
| 9 | `dast_zap` | OWASP ZAP | une regle en FAIL |
| 10 | `publish_image` | GHCR | (main uniquement) |
| 11 | `deploy_staging` | Docker + smoke test `/health` | (main uniquement) |
| 12 | `notify` | Discord | (toujours execute) |

Chaque job publie son rapport en artefact GitHub Actions. La branche `main` est protegee :
la fusion est impossible tant qu'un controle requis est rouge.

## Securite cote developpeur (shift-left)

- **pre-commit** : bloque en local un commit contenant un secret (Gitleaks) ou une faille MEDIUM+ (Bandit).
- **SonarQube for IDE** (ex-SonarLint) dans VS Code : detection en temps reel.

```bash
sudo apt install -y pre-commit
pre-commit install
```

## Lancer les controles en local

```bash
bash scripts/local-scan.sh        # Gitleaks, Bandit, Trivy, Checkov (necessite Docker)
pre-commit run --all-files        # hooks pre-commit sur tout le depot
```

## Lancer l'application

```bash
docker build -t devsecops-app .
docker run -d --name devsecops-app -p 5000:5000 -e SECRET_KEY=demo devsecops-app
curl localhost:5000/health        # {"status":"ok"}
```

## Secrets du pipeline

Definis dans GitHub (Settings > Secrets and variables > Actions > Repository secrets), jamais dans le code :

| Secret | Usage |
|---|---|
| `SECRET_KEY` | cle de l'application (deploiement staging) |
| `WEBHOOK_URL` | webhook Discord des notifications |

## Exemptions (faux positifs)

Procedure et modele de pull request : [docs/exemption-process.md](docs/exemption-process.md).
Suivi des vulnerabilites applicatives : [docs/security-tickets.md](docs/security-tickets.md).

## Etat as-is / to-be

- Tag `as-is-baseline` : application initiale, avec ses failles.
- Tag `to-be-secured` : application et pipeline securises.

```bash
git checkout as-is-baseline    # etat initial
git checkout to-be-secured     # etat securise
```
