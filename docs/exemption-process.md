# Procédure d'exemption exceptionnelle (faux positif bloquant)

Auteurs : Riadh Tarhouni et Balkis Baraket

## 1. Principe

Un contrôle de sécurité qui bloque le pipeline ne se contourne jamais en le désactivant.
Si le résultat est un **faux positif** ou un **risque accepté**, on crée une exemption
**ciblée, justifiée, datée et relue** par une personne autre que l'auteur, dans une pull request.
La décision reste ainsi traçable dans l'historique Git.

## 2. Étapes à suivre

1. **Vérifier** que le blocage est bien un faux positif (ou un risque accepté) :
   lire le rapport de l'outil (artefact du run GitHub Actions) et la règle concernée.
2. **Corriger** si une correction est possible. L'exemption est le dernier recours.
3. **Créer une branche** `exemption/<outil>-<sujet>`.
4. **Ajouter l'exemption la plus ciblée possible** (voir le tableau ci-dessous),
   avec un commentaire qui contient : la raison, la date, l'auteur, une date de revue.
5. **Ouvrir une pull request** dont la description reprend le modèle de la section 4.
6. **Faire relire** la PR par une deuxième personne. Les contrôles requis doivent passer.
7. **Fusionner** seulement après approbation. La PR et le commit forment la trace de la décision.
8. **Revoir** l'exemption à la date prévue. Si elle n'est plus nécessaire, la supprimer.

## 3. Où déclarer l'exemption, par outil

| Outil | Fichier / mécanisme | Portée |
|---|---|---|
| Gitleaks | `.gitleaks.toml` (allowlist) ou `gitleaks-baseline.json` | Une règle, un fichier ou une empreinte précise |
| Bandit | Commentaire `# nosec B<numéro>` sur la ligne, avec la raison | Une ligne |
| Trivy (dépendances/image) | `.trivyignore` (un identifiant CVE par ligne) ou `--ignore-unfixed` | Une CVE |
| Checkov | `#checkov:skip=CKV_xxx:raison` dans la ressource Terraform | Une ressource et une règle |
| OWASP ZAP | `.zap-rules.tsv` (règle en IGNORE) | Une règle |
| SonarQube | Statut « Accepted » / « Won't fix » avec commentaire dans l'interface | Une issue |

Règles :
- Une exemption ne couvre qu'un seul cas, jamais un dossier entier ni un outil entier.
- Une exemption sans raison écrite est refusée en revue.
- Les exemptions ne s'appliquent pas aux secrets réels : un vrai secret est **révoqué et remplacé**, pas exempté.

## 4. Modèle de description de pull request

```
Outil : <Gitleaks | Bandit | Trivy | Checkov | ZAP | SonarQube>
Règle / identifiant : <ex. CKV_AWS_18, CVE-2024-xxxx, B608>
Fichier concerné : <chemin>
Raison (pourquoi faux positif ou risque accepté) : ...
Mesure compensatoire (si applicable) : ...
Auteur : ...   Date : ...   Date de revue : ...
Relecteur : ...
```

## 5. Exemples déjà présents dans le projet

- **Checkov** : 5 contrôles Terraform ignorés avec `#checkov:skip` et une raison.
- **ZAP** : 2 règles en IGNORE dans `.zap-rules.tsv`, justifiées dans le fichier.
- **Trivy** : vulnérabilités sans correctif publié écartées avec `--ignore-unfixed`, car elles ne sont pas corrigeables aujourd'hui.
- **Gitleaks** : `gitleaks-baseline.json` pour les anciens faux positifs ; les nouvelles fuites restent bloquantes.

## 6. Traçabilité et audit

Chaque exemption est retrouvable avec `git log -p -- <fichier d'exemption>` et via la pull request associée.
Un audit peut ainsi savoir qui a accepté quoi, quand et pourquoi.
