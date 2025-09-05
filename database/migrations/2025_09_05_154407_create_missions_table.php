<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('missions', function (Blueprint $table) {
            $table->id();
            $table->string("uid")->nullable();
            $table->foreignId("proposer_id")->nullable()->constrained("users");
            $table->foreignId("contributor_id")->nullable()->constrained("users");
            $table->string("title")->nullable();
            $table->string("description")->nullable();
            $table->string("pictures")->nullable();
            $table->json("location")->nullable();
            $table->string("address")->nullable();
            $table->string("reward_amount")->nullable();
            $table->string("reward_currency")->nullable();
            $table->integer("duration")->nullable();
            $table->enum("status", ["pending", "accepted", "rejected", "ongoing", "completed", "cancelled"])->default("pending");
            $table->boolean("is_visible")->default(true);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('missions');
    }
};
