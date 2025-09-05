# API Documentation - Upload Controller

## Vue d'ensemble

L'API d'upload permet de télécharger un ou plusieurs fichiers sur le serveur et de récupérer les URLs publiques pour y accéder. Le contrôleur supporte l'upload de fichiers individuels ou multiples avec une validation robuste et une gestion d'erreurs complète.

## Endpoint

```
POST /api/upload
```

## Paramètres

### Upload d'un seul fichier

-   **file** (file, optionnel) : Un seul fichier à uploader
    -   Taille maximale : 10MB
    -   Types acceptés : Tous les types de fichiers

### Upload de plusieurs fichiers

-   **files** (array, optionnel) : Tableau de fichiers à uploader
    -   Nombre minimum : 1 fichier
    -   Nombre maximum : 10 fichiers
    -   Taille maximale par fichier : 10MB

**Note** : Vous devez fournir soit `file` soit `files`, mais pas les deux.

## Réponses

### Succès - Fichier unique (sans erreurs)

```json
{
    "success": true,
    "message": "Fichier uploadé avec succès",
    "file": {
        "original_name": "document.pdf",
        "file_name": "550e8400-e29b-41d4-a716-446655440000.pdf",
        "extension": "pdf",
        "size": 1024000,
        "url": "http://votre-domaine.com/storage/uploads/550e8400-e29b-41d4-a716-446655440000.pdf",
        "path": "uploads/550e8400-e29b-41d4-a716-446655440000.pdf"
    }
}
```

### Succès - Fichiers multiples (sans erreurs)

```json
{
    "success": true,
    "message": "Fichiers uploadés avec succès",
    "files": [
        {
            "original_name": "image1.jpg",
            "file_name": "550e8400-e29b-41d4-a716-446655440000.jpg",
            "extension": "jpg",
            "size": 512000,
            "url": "http://votre-domaine.com/storage/uploads/550e8400-e29b-41d4-a716-446655440000.jpg",
            "path": "uploads/550e8400-e29b-41d4-a716-446655440000.jpg"
        },
        {
            "original_name": "image2.png",
            "file_name": "550e8400-e29b-41d4-a716-446655440001.png",
            "extension": "png",
            "size": 256000,
            "url": "http://votre-domaine.com/storage/uploads/550e8400-e29b-41d4-a716-446655440001.png",
            "path": "uploads/550e8400-e29b-41d4-a716-446655440001.png"
        }
    ],
    "errors": [],
    "count": 2,
    "type": "multiple"
}
```

### Succès partiel - Certains fichiers uploadés avec erreurs

```json
{
    "success": true,
    "message": "Certains fichiers ont été uploadés avec des erreurs",
    "files": [
        {
            "original_name": "document.pdf",
            "file_name": "550e8400-e29b-41d4-a716-446655440000.pdf",
            "extension": "pdf",
            "size": 1024000,
            "url": "http://votre-domaine.com/storage/uploads/550e8400-e29b-41d4-a716-446655440000.pdf",
            "path": "uploads/550e8400-e29b-41d4-a716-446655440000.pdf"
        }
    ],
    "errors": [
        {
            "file": "trop-gros.pdf",
            "error": "File too large"
        }
    ],
    "count": 1,
    "type": "multiple"
}
```

### Erreur - Validation

```json
{
    "success": false,
    "message": "Erreur de validation",
    "errors": {
        "file": ["Le champ file est requis."],
        "files": ["Le champ files doit être un tableau."]
    }
}
```

### Erreur - Aucun fichier fourni

```json
{
    "success": false,
    "message": "Aucun fichier fourni. Utilisez \"file\" pour un seul fichier ou \"files\" pour plusieurs fichiers."
}
```

### Erreur - Aucun fichier uploadé

```json
{
    "success": false,
    "message": "Aucun fichier uploadé",
    "files": [],
    "errors": [
        {
            "file": "fichier-corrompu.txt",
            "error": "Erreur lors de l'upload"
        }
    ],
    "count": 0,
    "type": "multiple"
}
```

## Codes de statut HTTP

-   **200** : Succès (fichier(s) uploadé(s))
-   **400** : Erreur de requête (aucun fichier fourni, erreur de validation, aucun fichier uploadé)
-   **422** : Erreur de validation des données

## Exemples d'utilisation

### cURL - Upload d'un seul fichier

```bash
curl -X POST http://votre-domaine.com/api/upload \
  -F "file=@/chemin/vers/votre/fichier.pdf"
```

### cURL - Upload de plusieurs fichiers

```bash
curl -X POST http://votre-domaine.com/api/upload \
  -F "files[]=@/chemin/vers/image1.jpg" \
  -F "files[]=@/chemin/vers/image2.png" \
  -F "files[]=@/chemin/vers/document.pdf"
```

### JavaScript (Fetch API)

```javascript
// Upload d'un seul fichier
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("/api/upload", {
    method: "POST",
    body: formData,
})
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            console.log("Fichier uploadé:", data.file.url);
        } else {
            console.error("Erreur:", data.message);
        }
    });

// Upload de plusieurs fichiers
const formData = new FormData();
Array.from(fileInput.files).forEach((file) => {
    formData.append("files[]", file);
});

fetch("/api/upload", {
    method: "POST",
    body: formData,
})
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            console.log(`${data.count} fichier(s) uploadé(s)`);
            data.files.forEach((file) => {
                console.log("URL:", file.url);
            });
        } else {
            console.error("Erreur:", data.message);
        }
    });
```

## Caractéristiques

### Sécurité

-   Validation stricte des types de fichiers
-   Limitation de la taille des fichiers (10MB max)
-   Limitation du nombre de fichiers (10 max pour les uploads multiples)
-   Génération de noms de fichiers uniques avec UUID

### Stockage

-   Fichiers stockés dans `storage/app/public/uploads/`
-   URLs publiques générées automatiquement
-   Noms de fichiers originaux préservés dans la réponse

### Gestion d'erreurs

-   Validation robuste avec messages d'erreur détaillés
-   Gestion des erreurs individuelles par fichier
-   Support des uploads partiels (certains fichiers réussissent, d'autres échouent)

### Format de réponse

-   Structure de réponse cohérente
-   Différenciation entre uploads simples et multiples
-   Métadonnées complètes des fichiers uploadés
-   Compteurs et indicateurs de type de réponse
