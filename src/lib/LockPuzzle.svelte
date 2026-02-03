<script>
  import { tick } from 'svelte';
  import confetti from 'canvas-confetti';
  import { browser } from '$app/environment'; // Import browser environment check
  import { base } from '$app/paths';  

  export let code;
  export let answer;

  let inputCode = '';
  let isShaking = false;
  let isLoading = false;
  let isUnlocked = false;

  let inputRef;

  // Sound Effects
  // Initialize Audio only if browser
  let suspenseSound, successSound, errorSound;
  if (browser) {
    const prefix = base || ''; // base is '' locally, '/simple-escape' on GH Pages

    suspenseSound = new Audio(`${prefix}/sounds/add.wav`);
    errorSound    = new Audio(`${prefix}/sounds/error.wav`);
    successSound  = new Audio(`${prefix}/sounds/success.wav`);
  }

  // validate the code
  function validateCode() {
    if (!inputCode.trim()) {
      inputRef.focus();
      return;
    }

    // Play suspense sound
    if (browser) {
      suspenseSound.currentTime = 0;
      suspenseSound.play();
    }

    isLoading = true;

    setTimeout(async () => {
      if (browser) suspenseSound.pause();
      isLoading = false;

      if (inputCode === code) {
        isUnlocked = true;
        if (browser) successSound.play();
        launchConfetti();
      } else {
        if (browser) errorSound.play(); 
        triggerShake();
        inputCode = '';
        await tick();
        inputRef.focus();
      }
    }, Math.floor(Math.random() * 1500) + 1500);
  }

  function triggerShake() {
    isShaking = true;
    setTimeout(() => (isShaking = false), 600);
  }

  function launchConfetti() {
    confetti({
      particleCount: 120,
      spread: 70,
      origin: { y: 0.6 },
    });
  }

  function handleKeydown(event) {
    if (event.key === 'Enter') {
      validateCode();
    }
  }
</script>


<div class="flex flex-col items-center justify-center text-center h-screen text-white p-6 mb-10">
  {#if !isUnlocked}
    <!-- Padlock -->
    <div class="relative">
      <div class="text-8xl mb-8 animate-pulse">🔒</div>
      {#if isLoading}
        <!-- Intense Loading Animation -->
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="flex space-x-2 animate-fade-in">
            <div class="w-4 h-4 bg-indigo-500 rounded-full animate-bounce delay-0"></div>
            <div class="w-4 h-4 bg-indigo-400 rounded-full animate-bounce delay-150"></div>
            <div class="w-4 h-4 bg-indigo-300 rounded-full animate-bounce delay-300"></div>
          </div>
        </div>
      {/if}
    </div>

    <!-- Input Field -->
    <input
    type="text"
    maxlength="3"
    bind:value={inputCode}
    bind:this={inputRef}
    placeholder="***"
    autofocus
    disabled={isLoading}
    on:keydown={handleKeydown}
    class="w-40 p-3 text-5xl font-mono tracking-widest text-center bg-gray-800 text-indigo-300 
      border-4 border-gray-700 rounded-lg focus:outline-none focus:border-indigo-400 
      focus:ring-4 focus:ring-indigo-500/70 transition-all duration-300 ease-in-out 
      shadow-lg hover:shadow-indigo-400/40 {isShaking ? 'animate-shake' : 'animate-input-focus'} "
  />
  
    <!-- Submit Button -->
    <button
      on:click={validateCode}
      disabled={isLoading}
      class="mt-6 px-8 py-4 text-2xl font-bold text-white rounded-full 
        bg-gradient-to-r from-indigo-600 to-purple-500 hover:from-purple-500 hover:to-indigo-600 
        shadow-lg hover:shadow-indigo-500/50 transition-transform transform hover:scale-105
        active:scale-95 focus:outline-none animate-glow"
    >
      🚀 Open
    </button>
  {:else}
    <!-- Success Reveal -->
    <div class="text-6xl mb-6 animate-pulse">🎉</div>
    <div class="text-5xl font-bold animate-fade-in text-indigo-300">
      {answer}
    </div>
  {/if}
</div>

<style>

@keyframes input-focus {
  0%, 100% {
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.8);
  }
  50% {
    box-shadow: 0 0 20px rgba(99, 102, 241, 1), 0 0 30px rgba(99, 102, 241, 0.6);
  }
}

.animate-input-focus:focus {
  animation: input-focus 1.5s infinite ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 90% { transform: translateX(-10px); }
  20%, 80% { transform: translateX(10px); }
  30%, 50%, 70% { transform: translateX(-15px); }
  40%, 60% { transform: translateX(15px); }
}

.animate-shake {
  animation: shake 0.6s ease-in-out;
}


  /* Fade In */
  @keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fade-in {
    animation: fade-in 1s ease-out;
  }

  /* Bounce Loading Animation */
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  .animate-bounce {
    animation: bounce 1.2s infinite;
  }

  /* Delay for Loading Dots */
  .delay-0 { animation-delay: 0s; }
  .delay-150 { animation-delay: 0.15s; }
  .delay-300 { animation-delay: 0.3s; }

  /* Submit Button Glow */
  @keyframes glow {
    0% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.7); }
    50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.9); }
    100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.7); }
  }
  .animate-glow {
    animation: glow 1.5s infinite ease-in-out;
  }
</style>
