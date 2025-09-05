<?php

namespace App\Observers;

use App\Models\Mission;
use Illuminate\Support\Str;

class MissionObserver
{
    public function creating(Mission $mission): void
    {
        if ($mission->uid === null) {
            $mission->uid = Str::uuid();
        }
    }

    /**
     * Handle the Mission "created" event.
     */
    public function created(Mission $mission): void
    {
        //
    }

    /**
     * Handle the Mission "updated" event.
     */
    public function updated(Mission $mission): void
    {
        //
    }

    /**
     * Handle the Mission "deleted" event.
     */
    public function deleted(Mission $mission): void
    {
        //
    }

    /**
     * Handle the Mission "restored" event.
     */
    public function restored(Mission $mission): void
    {
        //
    }

    /**
     * Handle the Mission "force deleted" event.
     */
    public function forceDeleted(Mission $mission): void
    {
        //
    }
}
