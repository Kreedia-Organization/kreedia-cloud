<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class UploadController extends Controller
{
    /**
     * Upload un ou plusieurs fichiers et retourne les liens
     */
    public function upload(Request $request): JsonResponse
    {
        try {
            // Validation des fichiers - accepter soit 'file' soit 'files'
            $request->validate([
                'file' => 'sometimes|file|max:10240', // Un seul fichier
                'files' => 'sometimes|array|min:1|max:10', // Plusieurs fichiers
                'files.*' => 'required_with:files|file|max:10240', // 10MB max par fichier
            ], [
                'file.required_without' => 'Aucun fichier fourni. Utilisez "file" pour un seul fichier ou "files" pour plusieurs fichiers.',
                'files.required_without' => 'Aucun fichier fourni. Utilisez "file" pour un seul fichier ou "files" pour plusieurs fichiers.',
            ]);
        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json([
                'success' => false,
                'message' => 'Erreur de validation',
                'errors' => $e->errors()
            ], 422);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Erreur lors de la validation: ' . $e->getMessage()
            ], 400);
        }

        // Vérifier qu'au moins un fichier est fourni
        if (!$request->hasFile('file') && !$request->hasFile('files')) {
            return response()->json([
                'success' => false,
                'message' => 'Aucun fichier fourni. Utilisez "file" pour un seul fichier ou "files" pour plusieurs fichiers.'
            ], 400);
        }

        $uploadedFiles = [];
        $errors = [];
        $filesToProcess = [];

        // Déterminer quels fichiers traiter
        if ($request->hasFile('file')) {
            // Un seul fichier
            $filesToProcess = [$request->file('file')];
        } elseif ($request->hasFile('files')) {
            // Plusieurs fichiers
            $filesToProcess = $request->file('files');
        }

        foreach ($filesToProcess as $index => $file) {
            try {
                // Générer un nom unique pour le fichier
                $originalName = $file->getClientOriginalName();
                $extension = $file->getClientOriginalExtension();
                $fileName = Str::uuid() . '.' . $extension;

                // Stocker le fichier dans le dossier public
                $path = $file->storeAs('uploads', $fileName, 'public');

                // Générer l'URL publique
                $url = asset('storage/' . $path);

                $uploadedFiles[] = [
                    'original_name' => $originalName,
                    'file_name' => $fileName,
                    'extension' => $extension,
                    'size' => $file->getSize(),
                    'url' => $url,
                    'path' => $path
                ];
            } catch (\Exception $e) {
                $errors[] = [
                    'file' => $file->getClientOriginalName(),
                    'error' => $e->getMessage()
                ];
            }
        }

        // Déterminer le type de réponse selon le nombre de fichiers et la présence d'erreurs
        $isSingleFile = $request->hasFile('file') && !$request->hasFile('files');
        $hasErrors = !empty($errors);
        $hasUploadedFiles = count($uploadedFiles) > 0;

        // Si c'est un seul fichier et pas d'erreurs, retourner directement l'objet
        if ($isSingleFile && count($uploadedFiles) === 1 && !$hasErrors) {
            return response()->json([
                'success' => true,
                'message' => 'Fichier uploadé avec succès',
                'file' => $uploadedFiles[0]
            ], 200);
        }

        // Si plusieurs fichiers ou erreurs, retourner la liste
        $message = '';
        if ($hasUploadedFiles && !$hasErrors) {
            $message = $isSingleFile ? 'Fichier uploadé avec succès' : 'Fichiers uploadés avec succès';
        } elseif ($hasUploadedFiles && $hasErrors) {
            $message = 'Certains fichiers ont été uploadés avec des erreurs';
        } else {
            $message = 'Aucun fichier uploadé';
        }

        return response()->json([
            'success' => $hasUploadedFiles,
            'message' => $message,
            'files' => $uploadedFiles,
            'errors' => $errors,
            'count' => count($uploadedFiles),
            'type' => $isSingleFile ? 'single' : 'multiple'
        ], $hasUploadedFiles ? 200 : 400);
    }
}