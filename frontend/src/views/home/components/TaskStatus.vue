<script setup lang="ts">
import type { Command } from './types'

const props = defineProps<{ cmd: Command }>()

defineEmits<{ abort: [] }>()

const statusClasses: { [key in typeof props.cmd.status]: string } = {
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
      {{ props.cmd.name }}
    </div>

    <div class="flex items-center w-4/6 ps-1 py-1">
      <!-- status badget -->
      <div class="shrink-0 w-[4.1rem]">
        <span
          class="inline-flex justify-center items-center max-w-[96%] h-6 px-1 rounded"
          :class="statusClasses[props.cmd.status]"
        >
          <p class="text-sm truncate">{{ $t(`executeStatues.${props.cmd.status}`) }}</p>
        </span>
      </div>

      <!-- messages -->
      <template v-if="props.cmd.status == 'speeded' || props.cmd.status == 'failed'">
        <div class="text-sm break-all line-clamp-3">
          {{ $t('executeStatues.exitCode', { code: props.cmd.result?.exitCode }) }}

          <p v-if="props.cmd.status == 'speeded'" class="text-xs text-orange-300">
            {{
              $t('executeStatues.earlyExit', {
                second: `${(props.cmd.result?.lapse ?? -1).toFixed(1)}/${props.cmd.minExeTime}`
              })
            }}
          </p>
          <p
            v-else-if="
              props.cmd.result &&
              props.cmd.result.error !== '' &&
              !props.cmd.result.error.includes('exit status')
            "
            class="text-xs text-red-400 font-mono"
          >
            {{
              props.cmd.result.error.includes('file does not exist') ||
              props.cmd.result.error.includes('The system cannot find the file specified.') ||
              props.cmd.result.error.includes('The system cannot find the path specified.')
                ? $t('executeStatues.fileNotExist')
                : props.cmd.result.error.split(':').slice(1).join(':').trim()
            }}
          </p>
          <p v-else class="text-xs text-red-400 font-mono">
            {{ props.cmd.result?.stderr }}
          </p>
        </div>
      </template>

      <template v-else-if="props.cmd.status == 'broken'">
        <div class="text-sm break-all line-clamp-2 font-mono">
          {{
            props.cmd.result?.error?.split(':').slice(1).join(':').trim() ??
            $t('executeStatues.startFailed')
          }}
        </div>
      </template>

      <template v-else-if="props.cmd.status == 'completed'">
        <div class="text-xs text-gray-300 break-all line-clamp-2">
          {{
            $t('executeStatues.executeTime', {
              second: Math.round(props.cmd.result?.lapse ?? -1)
            })
          }}
        </div>
        <!-- <div class="text-xs break-all line-clamp-2">
          <p class="text-gray-400">
            狀態碼：{{ props.command.result?.exitCode }}；執行時間：{{
              Math.round(props.command.result?.lapse ?? -1)
            }}秒
          </p>

          <p
            class="font-mono"
            :class="
              props.command.result?.stderr !== '' ? 'text-red-400' : 'text-half-baked-400'
            "
            :title="props.command.result?.stderr || props.command.result?.stdout"
          >
            {{ props.command.result?.stderr || props.command.result?.stdout }}
          </p>
        </div> -->
      </template>

      <!-- abort button -->
      <button
        v-show="props.cmd.status == 'pending' || props.cmd.status == 'running'"
        class="ms-auto mx-1 px-1.5 text-sm bg-kashmir-blue-100 rounded"
        @click="$emit('abort')"
      >
        {{ $t('executeStatues.abort') }}
      </button>
    </div>
  </div>
</template>
