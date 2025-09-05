<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;

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
