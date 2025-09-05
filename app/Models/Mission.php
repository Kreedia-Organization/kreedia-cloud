<?php

namespace App\Models;

use App\Observers\MissionObserver;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([MissionObserver::class])]
class Mission extends BaseModel
{
    /** @use HasFactory<\Database\Factories\MissionFactory> */
    use HasFactory;

    protected $fillable = [
        'uid',
        'proposer_id',
        'title',
        'description',
        'pictures',
        'location',
        'address',
        'reward_amount',
        'reward_currency',
        'duration',
        'reward_token_amount',
        'status',
        'is_visible',
    ];

    protected static function booted()
    {
        static::addGlobalScope('globalScope', function ($query) {

            $query->orderBy('id', 'DESC');
        });
    }

    public function proposer(): BelongsTo
    {
        return $this->belongsTo(User::class, 'proposer_id');
    }
}
