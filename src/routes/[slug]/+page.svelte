<script>
    import { puzzles } from '$lib/puzzles.js';
    import LockPuzzle from '$lib/LockPuzzle.svelte';
    import { page } from '$app/stores';
  
    let puzzleData;
  
    // Find the current puzzle based on route parameters
    $: puzzleData = puzzles.find((p) => p.slug === $page.params.slug);
  
    function goBack() {
      history.back();
    }
  </script>
  
  {#if puzzleData}
  <div class="flex flex-col items-center justify-center h-screen bg-gray-900 text-white p-6 overflow-hidden">
    <!-- Back Button -->
      <button
        on:click={goBack}
        class="absolute top-4 left-4 flex items-center gap-2 text-indigo-400 hover:text-indigo-300 text-lg"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Terug
      </button>
  
      <!-- Puzzle Name -->
      <h1 class="text-5xl font-bold mt-10 text-center animate-fade-in">
        {puzzleData.name}
      </h1>
  
      <!-- Lock Puzzle -->
      <LockPuzzle code={puzzleData.code} answer={puzzleData.answer} />
    </div>
  {:else}
    <!-- Handle Invalid Slugs -->
    <div class="flex items-center justify-center min-h-screen bg-gray-900 text-white text-2xl">
      <p>Oeps! Deze puzzel bestaat niet. <a href="/" class="underline text-indigo-400">Terug naar start</a></p>
    </div>
  {/if}
  
  <style>
    @keyframes fade-in {
      0% {
        opacity: 0;
        transform: translateY(-10px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
      }
    }
    .animate-fade-in {
      animation: fade-in 0.8s ease-out;
    }
  </style>
  