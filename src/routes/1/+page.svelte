<script>
  import { puzzles } from '$lib/puzzles.js';
  import PuzzleCard from '$lib/PuzzleCard.svelte';

  // Assign emojis to each puzzle
  const emojiMap = {
    "Handen alfabet": "✋📚",
    "Woordzoeker": "🔍📝",
    "Rekenblokken": "🔢🧱",
    "Paardensprong": "♞🟦",
    "Welke stoel?": "🪑🤔",
    "Woord en cijfer": "🔠🔢",
    "Zoekplaat": "🖼️🔎"
  };
</script>

<main class="flex flex-col items-center min-h-screen bg-gray-900 text-white p-6">
  <!-- Title -->
  <h1 class="text-5xl font-bold mb-12 animate-fade-in">ONSTSNAP als je kunt!</h1>

  <!-- Puzzle Cards Grid -->
  <div class="grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 w-full max-w-7xl">
    {#each puzzles as puzzle}
      <PuzzleCard 
        name={puzzle.name}
        emoji={emojiMap[puzzle.name]}
        href={"1/" + puzzle.slug}
      />
    {/each}
  </div>
</main>

<style>
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .animate-fade-in {
    animation: fade-in 1s ease-out;
  }
</style>
