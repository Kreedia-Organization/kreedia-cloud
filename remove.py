import os
import subprocess
import time
from pathlib import Path
import re

def main():
    # Utilisation du chemin du dossier parent du script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    laravel_base_path = current_dir
    models_file_path = os.path.join(current_dir, 'model.txt')
    
    # Vérification du fichier artisan dans le dossier parent
    if not os.path.exists(os.path.join(current_dir, 'artisan')):
        print("Erreur: Ce script doit être placé dans la racine d'un projet Laravel")
        return
    
    # Vérification que le fichier model.txt existe
    if not os.path.exists(models_file_path):
        print(f"Erreur: Le fichier {models_file_path} n'existe pas.")
        return
    
    # Lecture des modèles à supprimer
    with open(models_file_path, 'r') as f:
        models = [line.strip() for line in f.readlines() if line.strip()]
    
    if not models:
        print("Aucun modèle trouvé dans le fichier model.txt")
        return
    
    print(f"Modèles à supprimer: {', '.join(models)}")
    
    # Confirmation avant suppression
    confirmation = input("\nAttention: Cette opération va supprimer tous les fichiers associés aux modèles listés (sauf les migrations).\nVoulez-vous continuer? (o/n): ")
    if confirmation.lower() not in ['o', 'oui', 'y', 'yes']:
        print("Opération annulée.")
        return
    
    # Suppression des fichiers pour chaque modèle
    for model in models:
        remove_model_files(laravel_base_path, model)
    
    print("\nSuppression terminée avec succès!")

def remove_model_files(laravel_base_path, model_name):
    """Supprime tous les fichiers associés à un modèle donné, sauf les migrations"""
    print(f"\nSuppression des fichiers pour {model_name}...")
    
    paths = {
        'model': os.path.join(laravel_base_path, 'app', 'Models'),
        'controller': os.path.join(laravel_base_path, 'app', 'Http', 'Controllers'),
        'seeder': os.path.join(laravel_base_path, 'database', 'seeders'),
        'observer': os.path.join(laravel_base_path, 'app', 'Observers'),
        'resource': os.path.join(laravel_base_path, 'app', 'Http', 'Resources'),
        'policy': os.path.join(laravel_base_path, 'app', 'Policies'),
        'factory': os.path.join(laravel_base_path, 'database', 'factories'),
        'requests': os.path.join(laravel_base_path, 'app', 'Http', 'Requests'),
    }
    
    # Suppression du modèle
    remove_file(os.path.join(paths['model'], f"{model_name}.php"))
    
    # Suppression du contrôleur
    remove_file(os.path.join(paths['controller'], f"{model_name}Controller.php"))
    
    # Suppression du seeder
    remove_file(os.path.join(paths['seeder'], f"{model_name}Seeder.php"))
    
    # Suppression de l'observer
    remove_file(os.path.join(paths['observer'], f"{model_name}Observer.php"))
    
    # Suppression de la resource
    remove_file(os.path.join(paths['resource'], f"{model_name}Resource.php"))
    
    # Suppression de la policy
    remove_file(os.path.join(paths['policy'], f"{model_name}Policy.php"))
    
    # Suppression de la factory
    remove_file(os.path.join(paths['factory'], f"{model_name}Factory.php"))
    
    # Suppression des requests
    remove_file(os.path.join(paths['requests'], f"Store{model_name}Request.php"))
    remove_file(os.path.join(paths['requests'], f"Update{model_name}Request.php"))
    
    # Note: Nous ne supprimons pas les migrations car elles sont datées et peuvent avoir été exécutées

def remove_file(file_path):
    """Supprime un fichier s'il existe"""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Fichier supprimé: {file_path}")
        except Exception as e:
            print(f"Erreur lors de la suppression de {file_path}: {e}")
    else:
        print(f"Fichier non trouvé: {file_path}")

if __name__ == "__main__":
    main()
