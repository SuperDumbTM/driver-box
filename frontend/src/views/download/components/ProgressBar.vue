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

// const progressWindow = computed(() => {
//   const indices = Array.from(Array(props.progresses.length).keys())

//   if (props.progresses.length <= 3) {
//     return indices
//   }

//   if (currentTask.value === null) {
//     return []
//   } else {
//     if ('1' == '1') {
//       return [1, 2, 3]
//     } else {
//       if (props.progresses.length - (currentTask.value + 1) < 3) {
//         // within last 3 tasks
//         return indices.slice(props.progresses.length - 3)
//       } else {
//         return indices.slice(currentTask.value, currentTask.value + 3)
//       }
//     }
//   }
// })
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

  <div class="flex justify-between">
    <!-- <template v-for="i in progressWindow" :key="i">
      <div v-show="i != 0 || props.progresses.length < 3" class="flex flex-col w-20 justify-center">
        <div
          class="flex items-center w-8 h-8 mx-auto text-lg text-white bg-apple-green-600 rounded-full"
        >
          <span class="text-white text-center w-full">
            <i class="fa fa-check w-full fill-current white"></i>
          </span>
        </div>

        <div class="pt-1 text-xs text-center">
          {{ props.progresses[i].Name }}
        </div>
      </div>

      <div class="flex grow align-center items-center align-middle content-center pb-4">
        <div class="flex-1 w-full bg-gray-200 rounded items-center align-middle align-center">
          <div
            class="text-xs leading-none py-1 text-center text-grey-darkest rounded"
            :class="[props.progresses[i].status == 'failed' ? 'bg-red-400' : 'bg-apple-green-700']"
            :style="{
              width: `${(props.progresses[i].Current / props.progresses[i].Total) * 100}%`
            }"
          ></div>
        </div>
      </div>
    </template> -->
  </div>
</template>
