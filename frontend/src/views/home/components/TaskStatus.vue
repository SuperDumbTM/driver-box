<script setup lang="ts">
import type { Process } from './types'

const props = defineProps<{ process: Process }>()

defineEmits<{ abort: [] }>()

const statusClasses: { [key in typeof props.process.status]: string } = {
  pending: 'bg-gray-300',
  running: 'bg-half-baked-500 animate-pulse',
  aborting: 'bg-yellow-400 animate-pulse',
  aborted: 'bg-yellow-400',
  speeded: 'bg-red-300',
  failed: 'bg-red-300',
  completed: 'bg-apple-green-600',
  broken: 'bg-red-700 text-white'
}
</script>

<template>
  <div class="flex min-h-9 border-t last:border-b border-kashmir-blue-100">
    <div class="content-center w-2/6 pe-1 text-xs truncate">
      <p class="font-medium truncate">{{ props.process.command.groupName }}</p>
      <p v-if="props.process.command.name" class="truncate">
        &nbsp;&nbsp;{{ `⤷ ${props.process.command.name}` }}
      </p>
    </div>

    <div class="flex items-center w-4/6 ps-1 py-1">
      <!-- status badget -->
      <div class="shrink-0 w-[4.1rem]">
        <span
          class="inline-flex justify-center items-center max-w-[96%] h-6 px-1 rounded"
          :class="statusClasses[props.process.status]"
        >
          <p class="text-sm truncate">{{ $t(`executeStatues.${props.process.status}`) }}</p>
        </span>
      </div>

      <!-- messages -->
      <template v-if="props.process.status == 'speeded' || props.process.status == 'failed'">
        <div class="text-sm break-all line-clamp-3">
          {{ $t('executeStatues.exitCode', { code: props.process.result?.exitCode }) }}

          <p v-if="props.process.status == 'speeded'" class="text-xs text-orange-300">
            {{
              $t('executeStatues.earlyExit', {
                second: `${(props.process.result?.lapse ?? -1).toFixed(1)}/${props.process.command.config.minExeTime}`
              })
            }}
          </p>
          <p
            v-else-if="
              props.process.result &&
              props.process.result.error !== '' &&
              !props.process.result.error.includes('exit status')
            "
            class="text-xs text-red-400 font-mono"
          >
            {{
              props.process.result.error.includes('file does not exist') ||
              props.process.result.error.includes('The system cannot find the file specified.') ||
              props.process.result.error.includes('The system cannot find the path specified.')
                ? $t('executeStatues.fileNotExist')
                : props.process.result.error.split(':').slice(1).join(':').trim()
            }}
          </p>
          <p v-else class="text-xs text-red-400 font-mono">
            {{ props.process.result?.stderr }}
          </p>
        </div>
      </template>

      <template v-else-if="props.process.status == 'broken'">
        <div class="text-sm break-all line-clamp-2 font-mono">
          {{
            props.process.result?.error?.split(':').slice(1).join(':').trim() ??
            $t('executeStatues.startFailed')
          }}
        </div>
      </template>

      <template v-else-if="props.process.status == 'completed'">
        <div class="text-xs text-gray-300">
          <p class="truncate">
            {{ $t('executeStatues.exitCode', { code: props.process.result?.exitCode }) }}
          </p>
          <p class="truncate">
            {{
              $t('executeStatues.executeTime', {
                second: Math.round(props.process.result?.lapse ?? -1)
              })
            }}
          </p>
        </div>
      </template>

      <!-- abort button -->
      <button
        v-show="props.process.status == 'pending' || props.process.status == 'running'"
        class="ms-auto mx-1 px-1.5 text-sm bg-kashmir-blue-100 rounded"
        @click="$emit('abort')"
      >
        {{ $t('executeStatues.abort') }}
      </button>
    </div>
  </div>
</template>
