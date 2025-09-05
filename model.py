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
    
    # Lecture des modèles à générer
    with open(models_file_path, 'r') as f:
        models = [line.strip() for line in f.readlines() if line.strip()]
    
    if not models:
        print("Aucun modèle trouvé dans le fichier model.txt")
        return
    
    print(f"Modèles à générer: {', '.join(models)}")
    
    # Génération des fichiers pour chaque modèle
    for model in models:
        generate_model_files(laravel_base_path, model)
    
    print("\nGénération terminée avec succès!")

def generate_model_files(laravel_base_path, model_name):
    """Génère tous les fichiers pour un modèle donné"""
    print(f"\nGénération des fichiers pour {model_name}...")
    
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
    
    # Création des dossiers s'ils n'existent pas
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    
    # Génération des fichiers
    generate_model_file(paths['model'], model_name)
    generate_controller_file(paths['controller'], model_name)
    generate_seeder_file(paths['seeder'], model_name)
    generate_observer_file(paths['observer'], model_name)
    generate_resource_file(paths['resource'], model_name)
    generate_policy_file(paths['policy'], model_name)
    generate_factory_file(paths['factory'], model_name)
    generate_request_files(paths['requests'], model_name)
    
    # Génération automatique de la migration sans demander le nom
    generate_migration(laravel_base_path, model_name)

def generate_model_file(path, model_name):
    """Génère le fichier de modèle"""
    # Vérifier si BaseModel.php existe, sinon le créer
    base_model_path = os.path.join(path, 'BaseModel.php')
    if not os.path.exists(base_model_path):
        base_model_content = """<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\Concerns\\HasUuids;

abstract class BaseModel extends Model
{
    use HasUuids;

    public static function findByUid(string $uid): ?self
    {
        return self::where('uid', $uid)->first();
    }

    public function uniqueIds(): array
    {
        return ['uid'];
    }

    public function getRouteKeyName(): string
    {
        return 'uid';
    }
}
"""
        write_file(base_model_path, base_model_content)

    # Générer le modèle qui étend BaseModel
    file_path = os.path.join(path, f"{model_name}.php")
    content = f"""<?php

namespace App\\Models;

use App\\Observers\\{model_name}Observer;
use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Attributes\\ObservedBy;

#[ObservedBy([{model_name}Observer::class])]
class {model_name} extends BaseModel
{{
    /** @use HasFactory<\\Database\\Factories\\{model_name}Factory> */
    use HasFactory;

    protected $fillable = [
        'uid',
    ];

      protected static function booted()
    {{
        static::addGlobalScope('globalScope', function ($query) {{

            $query->orderBy('id', 'DESC');
        }});
    }}
}}
"""
    write_file(file_path, content)

def generate_controller_file(path, model_name):
    """Génère le fichier de contrôleur"""
    file_path = os.path.join(path, f"{model_name}Controller.php")
    
    content = f"""<?php

namespace App\\Http\\Controllers;

use App\\Models\\{model_name};
use Illuminate\\Http\\Request;
use App\\Http\\Requests\\Store{model_name}Request;
use App\\Http\\Requests\\Update{model_name}Request;

class {model_name}Controller extends Controller
{{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {{
        //
    }}

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {{
        //
    }}

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {{
        //
    }}

    /**
     * Display the specified resource.
     */
    public function show({model_name} ${model_name.lower()})
    {{
        //
    }}

    /**
     * Show the form for editing the specified resource.
     */
    public function edit({model_name} ${model_name.lower()})
    {{
        //
    }}

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, {model_name} ${model_name.lower()})
    {{
        //
    }}

    /**
     * Remove the specified resource from storage.
     */
    public function destroy({model_name} ${model_name.lower()})
    {{
        //
    }}
}}
"""
    write_file(file_path, content)

def generate_seeder_file(path, model_name):
    """Génère le fichier de seeder"""
    file_path = os.path.join(path, f"{model_name}Seeder.php")
    
    content = f"""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Console\\Seeds\\WithoutModelEvents;
use Illuminate\\Database\\Seeder;

class {model_name}Seeder extends Seeder
{{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {{
        //
    }}
}}
"""
    write_file(file_path, content)

def generate_observer_file(path, model_name):
    """Génère le fichier d'observer avec vérification de l'uid"""
    file_path = os.path.join(path, f"{model_name}Observer.php")
    content = f"""<?php

namespace App\\Observers;

use App\\Models\\{model_name};
use Illuminate\\Support\\Str;

class {model_name}Observer
{{
    public function creating({model_name} ${model_name.lower()}): void
    {{
        if (${model_name.lower()}->uid === null) {{
            ${model_name.lower()}->uid = Str::uuid();
        }}
    }}

    /**
     * Handle the {model_name} "created" event.
     */
    public function created({model_name} ${model_name.lower()}): void
    {{
        //
    }}

    /**
     * Handle the {model_name} "updated" event.
     */
    public function updated({model_name} ${model_name.lower()}): void
    {{
        //
    }}

    /**
     * Handle the {model_name} "deleted" event.
     */
    public function deleted({model_name} ${model_name.lower()}): void
    {{
        //
    }}

    /**
     * Handle the {model_name} "restored" event.
     */
    public function restored({model_name} ${model_name.lower()}): void
    {{
        //
    }}

    /**
     * Handle the {model_name} "force deleted" event.
     */
    public function forceDeleted({model_name} ${model_name.lower()}): void
    {{
        //
    }}
}}
"""
    write_file(file_path, content)

def generate_resource_file(path, model_name):
    """Génère le fichier de ressource"""
    file_path = os.path.join(path, f"{model_name}Resource.php")
    
    content = f"""<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class {model_name}Resource extends JsonResource
{{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {{
        return parent::toArray($request);
    }}
}}
"""
    write_file(file_path, content)

def generate_policy_file(path, model_name):
    """Génère le fichier de policy"""
    file_path = os.path.join(path, f"{model_name}Policy.php")
    
    content = f"""<?php

namespace App\\Policies;

use App\\Models\\{model_name};
use App\\Models\\User;
use Illuminate\\Auth\\Access\\Response;

class {model_name}Policy
{{
    /**
     * Determine whether the user can view any models.
     */
    public function viewAny(User $user): bool
    {{
        return true;
    }}

    /**
     * Determine whether the user can view the model.
     */
    public function view(User $user, {model_name} ${model_name.lower()}): bool
    {{
        return true;
    }}

    /**
     * Determine whether the user can create models.
     */
    public function create(User $user): bool
    {{
        return true;
    }}

    /**
     * Determine whether the user can update the model.
     */
    public function update(User $user, {model_name} ${model_name.lower()}): bool
    {{
        return true;
    }}

    /**
     * Determine whether the user can delete the model.
     */
    public function delete(User $user, {model_name} ${model_name.lower()}): bool
    {{
        return true;
    }}

    /**
     * Determine whether the user can restore the model.
     */
    public function restore(User $user, {model_name} ${model_name.lower()}): bool
    {{
        return true;
    }}

    /**
     * Determine whether the user can permanently delete the model.
     */
    public function forceDelete(User $user, {model_name} ${model_name.lower()}): bool
    {{
        return true;
    }}
}}
"""
    write_file(file_path, content)

def generate_factory_file(path, model_name):
    """Génère le fichier de factory"""
    file_path = os.path.join(path, f"{model_name}Factory.php")
    
    content = f"""<?php

namespace Database\\Factories;

use Illuminate\\Database\\Eloquent\\Factories\\Factory;

/**
 * @extends \\Illuminate\\Database\\Eloquent\\Factories\\Factory<\\App\\Models\\{model_name}>
 */
class {model_name}Factory extends Factory
{{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {{
        return [
            //
        ];
    }}
}}
"""
    write_file(file_path, content)

def generate_request_files(path, model_name):
    """Génère les fichiers de requête Store et Update"""
    os.makedirs(path, exist_ok=True)
    
    # StoreRequest
    store_content = f"""<?php

namespace App\\Http\\Requests;

use Illuminate\\Foundation\\Http\\FormRequest;

class Store{model_name}Request extends FormRequest
{{
    public function authorize(): bool
    {{
        return true;
    }}

    public function rules(): array
    {{
        return [
            //
        ];
    }}
}}
"""
    write_file(os.path.join(path, f"Store{model_name}Request.php"), store_content)
    
    # UpdateRequest
    update_content = f"""<?php

namespace App\\Http\\Requests;

use Illuminate\\Foundation\\Http\\FormRequest;

class Update{model_name}Request extends FormRequest
{{
    public function authorize(): bool
    {{
        return true;
    }}

    public function rules(): array
    {{
        return [
            //
        ];
    }}
}}
"""
    write_file(os.path.join(path, f"Update{model_name}Request.php"), update_content)

def generate_migration(laravel_path, model_name):
    """Génère une migration automatiquement avec un nom correct au pluriel"""
    # Convertit CamelCase en snake_case
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    # Pluralisation simple
    def pluralize(name):
        if name.endswith('y') and not name.endswith(('ay', 'ey', 'iy', 'oy', 'uy')):
            return name[:-1] + 'ies'
        elif name.endswith('s'):
            return name + 'es'
        else:
            return name + 's'

    snake_name = camel_to_snake(model_name)
    plural_name = pluralize(snake_name)
    migration_name = f"create_{plural_name}_table"

    try:
        os.chdir(laravel_path)
        subprocess.run(['php', 'artisan', 'make:migration', migration_name], check=True)
        print(f"Migration '{migration_name}' créée avec succès.")
        time.sleep(1)  # Attente d'une seconde après la création de la migration
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création de la migration: {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")

def write_file(file_path, content):
    """Écrit le contenu dans un fichier"""
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Fichier créé: {file_path}")

if __name__ == "__main__":
    main()