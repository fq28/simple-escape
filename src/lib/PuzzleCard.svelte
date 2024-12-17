<script>
    export let name; // Puzzle name
    export let emoji; // Emoji for the puzzle
    export let href; // Link to puzzle page
  </script>
  
  <a
    href={href}
    class="relative flex flex-col items-center justify-center h-60 p-4 bg-white text-gray-800 
      rounded-xl shadow-md cursor-pointer transform transition duration-300 
      hover:scale-105 hover:shadow-2xl hover:glimmer"
  >
    <!-- Emoji Icon -->
    <div class="text-7xl mb-2 drop-shadow-md">{emoji}</div>
  
    <!-- Puzzle Name -->
    <div class="text-3xl font-bold">{name}</div>
  
    <!-- Gleam Effect -->
    <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent 
        opacity-0 hover:opacity-100 transition duration-500 pointer-events-none rounded-xl"
    ></div>
  </a>
  
  <style>


  </style>
  