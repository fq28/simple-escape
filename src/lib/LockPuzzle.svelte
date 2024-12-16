<script>
    import confetti from "canvas-confetti";
  
    export let code; // The correct code (e.g., "123")
    export let answer; // The answer to reveal (e.g., "A")
    let inputCode = ""; // Tracks the user's input
    let isShaking = false;
    let isUnlocked = false;
  
    function validateCode() {
      if (inputCode === code) {
        isUnlocked = true;
        launchConfetti(); // Trigger confetti when unlocked
      } else {
        // Trigger the shake animation
        isShaking = true;
        setTimeout(() => (isShaking = false), 500);
        // Clear the input
        inputCode = "";
      }
    }
  
    function launchConfetti() {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      });
  
      // Additional burst effect
      setTimeout(() => {
        confetti({
          particleCount: 50,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
        });
  
        confetti({
          particleCount: 50,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
        });
      }, 500);
    }
  </script>
  
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
    {#if !isUnlocked}
      <!-- Padlock and Input -->
      <div class="text-center">
        <div class="text-6xl mb-4">🔒</div>
        <input
          type="text"
          maxlength="3"
          bind:value={inputCode}
          placeholder="code..."
          class="p-3 text-lg border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500
          text-gray-800 bg-white transition-transform duration-150 ease-in-out
          {isShaking ? 'animate-shake' : ''}"
        />
        <button
          on:click={validateCode}
          class="mt-4 px-6 py-2 bg-indigo-600 hover:bg-indigo-500 rounded text-lg"
        >
        ↵
        </button>
      </div>
    {/if}
  
    {#if isUnlocked}
      <!-- Reveal the Answer -->
      <div class="text-center">
        <div class="text-6xl mb-6 animate-pulse">🎉</div>
        <div
          class="text-4xl font-bold transition-opacity duration-500 opacity-100 animate-particles"
        >
         {answer}
        </div>
      </div>
    {/if}
  </div>
  
  <style>
    /* Shake animation */
    @keyframes shake {
      0%,
      100% {
        transform: translateX(0);
      }
      25% {
        transform: translateX(-5px);
      }
      50% {
        transform: translateX(5px);
      }
    }
  
    .animate-shake {
      animation: shake 0.5s ease-in-out;
    }
  
    /* Particle effect (optional, customize as needed) */
    @keyframes particles {
      0% {
        opacity: 0;
        transform: translateY(10px) scale(0.95);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
  
    .animate-particles {
      animation: particles 0.7s ease-out;
    }
  </style>
  