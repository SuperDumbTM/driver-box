<script setup lang="ts">
import CrossIcon from '@/components/icons/CrossIcon.vue'
import * as executor from '@/wailsjs/go/execute/CommandExecutor'
import * as runtime from '@/wailsjs/runtime/runtime'
import AsyncLock from 'async-lock'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toast-notification'
import TaskStatus from './TaskStatus.vue'
import type { Command, Process } from './types'

defineExpose({
  show: async (isParallel_: boolean, cmds: Array<Command>) => {
    show.value = true
    isParallel = isParallel_

    processes.value = cmds.map(vals => ({ command: { ...vals }, status: 'pending' }))
    dispatchCommand()
  },
  hide: () => {
    show.value = false
  }
})

const emit = defineEmits<{ completed: [] }>()

let isParallel = false

const { t } = useI18n()

const lock = new AsyncLock()

const $toast = useToast({ position: 'top-left', duration: 7000 })

const show = ref(false)

const processes = ref<Array<Process>>([])

runtime.EventsOn('execute:exited', async (id: string, result: NonNullable<Process['result']>) => {
  const process = processes.value.find(c => c.procId === id)!
  process.result = result

  if (result.aborted) {
    process.status = 'aborted'
  } else if (![0, ...process.command.config.allowRtCodes].includes(result.exitCode)) {
    process.status = 'failed'
  } else if (result.lapse < process.command.config.minExeTime) {
    process.status = 'speeded'
  } else {
    process.status = 'completed'
  }

  dispatchCommand().then(() => {
    if (processes.value.every(c => c.status === 'completed')) {
      emit('completed')
      $toast.success(t('toasts.finished'), { position: 'bottom-right' })
    } else if (processes.value.every(c => !c.status.includes('ing'))) {
      $toast.info(t('toasts.finished'), { position: 'bottom-right' })
    }
  })
})

function getProcessName(process: Process) {
  return process.command.name
    ? `${process.command.groupName} - ${process.command.name}`
    : process.command.groupName
}

async function dispatchCommand() {
  lock.acquire('executor', async () => {
    const pendings = processes.value
      .filter(c => c.status === 'pending')
      .slice(0, isParallel ? undefined : 1)

    for (const process of pendings) {
      if (
        !process.command.config.incompatibles.every(id =>
          processes.value.filter(p => p.status === 'running').every(p => p.command.id != id)
        )
      ) {
        continue
      }

      await executor
        .Run(process.command.config.program, process.command.config.options)
        .then(processId => {
          process.status = 'running'
          process.procId = processId
        })
        .catch(error => {
          process.status = 'broken'
          process.result = {
            lapse: -1,
            exitCode: -1,
            stdout: '',
            stderr: '',
            error: (error as Error).toString(),
            aborted: false
          }
        })
    }
  })
}

function handleAbort(process: Process) {
  return lock
    .acquire('executor', () => {
      if (process.status == 'pending' || process.status == 'running') {
        process.status =
          process.procId == undefined || process.procId == '' ? 'aborted' : 'aborting'
      }
    })
    .then(() => {
      if (process.status != 'aborting') {
        return
      }

      // `aborted` status will be updated at `execute:exited` event handler
      executor.Abort(process.procId!).catch(error => {
        if (error.includes('process does not exist')) {
          $toast.warning(
            t('toasts.cancelCompletedFailed', {
              name: getProcessName(process)
            })
          )
          return
        }

        error
          .toString()
          .split('\n')
          .forEach((err: string) => {
            if (err.includes('abort failed')) {
              $toast.warning(
                t('toasts.cancelFailed', {
                  name: getProcessName(process)
                })
              )
            } else {
              $toast.error(`[${getProcessName(process)}] ${err}`)
            }
          })

        process.status = 'broken'
        process.result = {
          lapse: -1,
          exitCode: -1,
          stdout: '',
          stderr: '',
          error: error.toString(),
          aborted: false
        }
      })
    })
}
</script>

<template>
  <Transition name="modal">
    <div class="bg-gray-900/50 fixed inset-0 z-40" v-show="show"></div>
  </Transition>

  <Transition name="modal">
    <div
      class="fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full h-full"
      v-show="show"
    >
      <div class="w-[65vw] max-w-3xl max-h-full p-4">
        <!-- Modal content -->
        <div class="bg-white rounded shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between px-3 py-1.5 border-b rounded-t bg-white">
            <h3 class="font-semibold">
              {{ $t('executeStatues.title') }}
            </h3>
            <button
              type="button"
              class="inline-flex justify-center items-center h-8 w-8 ms-auto text-sm text-gray-400 enabled:hover:text-gray-900 bg-transparent enabled:hover:bg-gray-200 rounded-lg"
              @click="
                () => {
                  show = false
                }
              "
              :disabled="
                processes.some(cmd => ['pending', 'running', 'aborting'].includes(cmd.status))
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="max-h-[70vh] overflow-y-auto py-2 px-4">
            <template v-for="(process, i) in processes" :key="i">
              <TaskStatus :process="process" @abort="handleAbort(process)"></TaskStatus>
            </template>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.5s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
