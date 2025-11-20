<script lang="ts">
  import { browser } from '$app/environment';
  import { base } from '$app/paths';
  import confetti from 'canvas-confetti';
  import { tick } from 'svelte';

  // 👉 Define your 3 locks here
  const locks = [
    {
      id: 1,
      title: 'Slot 1',
      description: 'De geheime ASCII boodschap',
      code: 'Bit 2',          // expected answer (text)
      placeholder: 'tekst'
    },
    {
      id: 2,
      title: 'Slot 2',
      description: 'Rekenen met letters',
      code: 'D',          // expected answer (text)
      placeholder: 'letter'
    },
    {
      id: 3,
      title: 'Slot 3',
      description: 'Unicode: verborgen teken',
      code: '菐',    // expected answer (text)
      placeholder: 'symbool'
    }
  ];

  const prefix = base ?? '';

  // Per-lock state
  type LockState = {
    input: string;
    isLoading: boolean;
    isUnlocked: boolean;
    isShaking: boolean;
  };

  let lockStates: LockState[] = locks.map(() => ({
    input: '',
    isLoading: false,
    isUnlocked: false,
    isShaking: false
  }));

  let inputRefs: HTMLInputElement[] = [];

  // Sounds
  let suspenseSound: HTMLAudioElement | undefined;
  let successSound: HTMLAudioElement | undefined;
  let errorSound: HTMLAudioElement | undefined;

  if (browser) {
    suspenseSound = new Audio(`${prefix}/sounds/add.wav`);
    errorSound = new Audio(`${prefix}/sounds/error.wav`);
    successSound = new Audio(`${prefix}/sounds/success.wav`);
  }

  // Derived: are all 3 locks open?
  $: allUnlocked = lockStates.every((l) => l.isUnlocked);

  function playSuspense() {
    if (!browser || !suspenseSound) return;
    suspenseSound.currentTime = 0;
    suspenseSound.play();
  }

  function stopSuspense() {
    if (!browser || !suspenseSound) return;
    suspenseSound.pause();
  }

  function playSuccess() {
    if (!browser || !successSound) return;
    successSound.currentTime = 0;
    successSound.play();
  }

  function playError() {
    if (!browser || !errorSound) return;
    errorSound.currentTime = 0;
    errorSound.play();
  }

  function launchConfettiGrand() {
    if (!browser) return;
    confetti({
      particleCount: 250,
      spread: 100,
      origin: { y: 0.5 }
    });
  }

  function triggerShake(index: number) {
    lockStates[index].isShaking = true;
    lockStates = [...lockStates];
    setTimeout(() => {
      lockStates[index].isShaking = false;
      lockStates = [...lockStates];
    }, 600);
  }

  async function validateLock(index: number) {
    const state = lockStates[index];
    const lock = locks[index];

    if (state.isLoading || state.isUnlocked) {
      return;
    }

    if (!state.input.trim()) {
      inputRefs[index]?.focus();
      return;
    }

    // Start suspense
    playSuspense();
    state.isLoading = true;
    lockStates = [...lockStates];

    const delay = Math.floor(Math.random() * 1500) + 1500;

    setTimeout(async () => {
      stopSuspense();
      state.isLoading = false;

      const expected = lock.code.trim().toLowerCase();
      const actual = state.input.trim().toLowerCase();

      if (actual === expected) {
        state.isUnlocked = true;
        lockStates = [...lockStates];

        playSuccess();

        if (lockStates.every((l) => l.isUnlocked)) {
          // Slight delay so they see the last lock open, then GRAND BOOM
          setTimeout(() => {
            launchConfettiGrand();
          }, 700);
        }
      } else {
        playError();
        state.input = '';
        lockStates = [...lockStates];
        triggerShake(index);

        await tick();
        inputRefs[index]?.focus();
      }
    }, delay);
  }

  function handleKeydown(index: number, event: KeyboardEvent) {
    if (event.key === 'Enter') {
      validateLock(index);
    }
  }
</script>

<main class="flex flex-col items-center min-h-screen bg-gray-900 text-white p-6">
  <!-- Title -->
  <h1 class="text-5xl font-bold mb-4 text-center animate-fade-in">
    ASCII &amp; Unicode Puzzel
  </h1>
  <p class="text-2xl mb-10 text-center max-w-2xl text-indigo-200">
    Los alle drie de sloten op.  
    Pas als <span class="font-bold text-indigo-400">alle codes</span> kloppen, onthult zich de echte beloning.
  </p>

  <!-- Locks grid -->
  {#if !allUnlocked}
    <section class="grid gap-8 w-full max-w-5xl grid-cols-1 md:grid-cols-3">
      {#each locks as lock, i}
        <div
          class="relative flex flex-col items-center justify-between bg-gray-800 rounded-2xl shadow-xl p-6
                 border border-gray-700 hover:border-indigo-400 transition-all duration-300
                 {lockStates[i].isUnlocked ? 'ring-2 ring-emerald-400/80' : ''}"
        >
          <!-- Lock icon + loading overlay -->
          <div class="relative mb-4 flex flex-col items-center">
            <div class="text-6xl mb-2 animate-pulse">
              {#if lockStates[i].isUnlocked}
                🔓
              {:else}
                🔒
              {/if}
            </div>

            {#if lockStates[i].isLoading}
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="flex space-x-2 animate-fade-in">
                  <div class="w-3 h-3 bg-indigo-500 rounded-full animate-bounce delay-0"></div>
                  <div class="w-3 h-3 bg-indigo-400 rounded-full animate-bounce delay-150"></div>
                  <div class="w-3 h-3 bg-indigo-300 rounded-full animate-bounce delay-300"></div>
                </div>
              </div>
            {/if}
          </div>

          <!-- Title & description -->
          <h2 class="text-3xl font-bold mb-2 text-center">{lock.title}</h2>
          <p class="text-lg mb-4 text-center text-indigo-200">
            {lock.description}
          </p>

          <!-- Input -->
          <input
            type="text"
            bind:value={lockStates[i].input}
            bind:this={inputRefs[i]}
            placeholder={lock.placeholder}
            disabled={lockStates[i].isLoading || lockStates[i].isUnlocked}
            on:keydown={(e) => handleKeydown(i, e)}
            class="w-full p-3 text-2xl md:text-xl font-mono text-center bg-gray-900 text-indigo-200 
                   border-2 border-gray-700 rounded-lg focus:outline-none focus:border-indigo-400 
                   focus:ring-4 focus:ring-indigo-500/70 transition-all duration-300 ease-in-out 
                   shadow-lg hover:shadow-indigo-400/40
                   {lockStates[i].isShaking ? 'animate-shake' : 'animate-input-focus'}"
          />

          <!-- Button -->
          <button
            on:click={() => validateLock(i)}
            disabled={lockStates[i].isLoading || lockStates[i].isUnlocked}
            class="mt-4 px-5 py-3 text-xl font-bold text-white rounded-full 
                   bg-gradient-to-r from-indigo-600 to-purple-500 
                   hover:from-purple-500 hover:to-indigo-600 
                   shadow-lg hover:shadow-indigo-500/50 
                   transition-transform transform hover:scale-105
                   active:scale-95 focus:outline-none animate-glow
                   disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if lockStates[i].isUnlocked}
              ✅ Geopend
            {:else if lockStates[i].isLoading}
              ⏳ Controleren...
            {:else}
              🚀 Open slot
            {/if}
          </button>
        </div>
      {/each}
    </section>
  {/if}

  <!-- Grand reward -->
  {#if allUnlocked}
    <section class="mt-12 text-center animate-fade-in-slow">
      <div class="text-7xl mb-4">🎉🎉🎉</div>
      <h2 class="text-4xl md:text-5xl font-bold text-emerald-300 mb-4">
        Jullie hebben alle sloten gekraakt!
      </h2>
      <p class="text-2xl md:text-3xl text-indigo-100 max-w-3xl mx-auto">
        Hier komt jullie ultieme beloning te staan:<br />
        <span class="font-semibold text-white">
          bijvoorbeeld een geheime zin, link, of hint naar de volgende uitdaging.
        </span>
      </p>
    </section>
  {/if}
</main>

<style>
  @keyframes input-focus {
    0%, 100% {
      box-shadow: 0 0 10px rgba(99, 102, 241, 0.8);
    }
    50% {
      box-shadow:
        0 0 20px rgba(99, 102, 241, 1),
        0 0 30px rgba(99, 102, 241, 0.6);
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

  @keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fade-in {
    animation: fade-in 0.8s ease-out;
  }

  @keyframes fade-in-slow {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fade-in-slow {
    animation: fade-in-slow 1.2s ease-out;
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  .animate-bounce {
    animation: bounce 1.2s infinite;
  }

  .delay-0 { animation-delay: 0s; }
  .delay-150 { animation-delay: 0.15s; }
  .delay-300 { animation-delay: 0.3s; }

  @keyframes glow {
    0% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.7); }
    50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.9); }
    100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.7); }
  }
  .animate-glow {
    animation: glow 1.5s infinite ease-in-out;
  }
</style>
