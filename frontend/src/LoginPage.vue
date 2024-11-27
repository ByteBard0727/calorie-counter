<template>
    <div class="max-w-sm mx-auto pt-20 flex items-center justify-center">
      <p class="absolute top-5 font-semibold text-3xl">Login</p>
  
  <!-- Horizontal line outside the container to take full width -->
  <hr class="border-t-2 border-gray-200 mb-8 w-full absolute top-20 left-0" />
  
      <form action="" class="w-full max-w-md">
        <!-- Horizontal line -->
        <hr class="border-t-2 border-gray-300 mb-8 w-full" />
  
        <!-- Email Input -->
        <div class="mb-6 pt-20">
          <label for="email" class="block mb-2">Email</label>
          <input
            type="email"
            id="email"
            class="bg-gray-300 text-sm px-4 py-2 w-full"
            placeholder="Enter your email"
            required
          />
        </div>
  
        <!-- Password Input -->
        <div class="mb-6">
          <label for="password" class="block mb-2">Password</label>
          <input
            type="password"
            id="password"
            class="bg-gray-300 text-sm px-4 py-2 w-full"
            placeholder="Enter your password"
            required
          />
        </div>
  
        <!-- Login Link -->
        <div class="text-start mb-6">
          <router-link to="/RegisterPage" class="text-gray-500 underline hover:text-blue-700">
            &gt; Register
          </router-link>
        </div>
  
        <!-- Register Button -->
        <div class="text-end">
          <button
            type="submit"
            class="bg-green-400 px-6 py-2 text-white font-semibold"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  </script>