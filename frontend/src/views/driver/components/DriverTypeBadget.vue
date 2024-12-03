<script setup lang="ts">
import type { store } from '@/wailsjs/go/models'

defineProps<{ type: store.DriverType }>()

const colors = {
  network: 'bg-blue-100',
  display: 'bg-green-100',
  miscellaneous: 'bg-gray-100'
}
</script>

<template>
  <span class="content-center me-1 px-1.5 h-5 text-xs text-nowrap rounded" :class="colors[type]">
    {{ $t(`driverForms.${type}`) }}
  </span>
</template>
