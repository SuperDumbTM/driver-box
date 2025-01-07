<script setup lang="ts">
import { statusBadget } from '@/definitions/styles'
import { porter } from '@/wailsjs/go/models'
import { computed } from 'vue'

const props = defineProps<{ progresses: porter.Progresses | null }>()

const currentTask = computed(() => {
  if (props.progresses === null || props.progresses.tasks.length == 0) {
    return null
  }

  for (const [i, progress] of props.progresses.tasks.entries()) {
    if (i > 0 && progress.status == 'pending') {
      return props.progresses.tasks[i - 1]
    }

    if (['pending', 'running'].includes(progress.status)) {
      return props.progresses.tasks[i]
    }
  }
  return props.progresses.tasks[props.progresses.tasks.length - 1]
})

const progress = computed(() => {
  if (currentTask.value === null) {
    return Number.NaN
  }
  return Math.floor((currentTask.value.current / currentTask.value.total) * 100)
})
</script>

<template>
  <div class="flex flex-col gap-y-2">
    <div class="flex justify-between">
      <div class="flex" v-if="progresses !== null && currentTask">
        <div class="shrink-0 w-[4.1rem]">
          <p
            class="inline-flex justify-center items-center max-w-[96%] h-6 px-1 rounded"
            :class="[
              { 'animate-pulse': progresses.status.includes('ing') },
              statusBadget[progresses.status as keyof typeof statusBadget]
            ]"
          >
            <span class="text-sm truncate">{{ $t(`executeStatus.${progresses.status}`) }}</span>
          </p>
        </div>

        <span class="font-medium">
          {{ $t(`porter.${currentTask.name}`) }}
        </span>
      </div>

      <span class="text-sm font-medium"> {{ Number.isNaN(progress) ? '--' : progress }} % </span>
    </div>

    <div class="w-full h-2.5 bg-gray-200 rounded-full">
      <div
        class="h-full bg-apple-green-700 rounded-full transition-all"
        :style="{ width: `${progress}%` }"
      ></div>
    </div>
  </div>
</template>
