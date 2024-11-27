<script setup lang="ts">
import CrossIcon from '@/components/icons/CrossIcon.vue'
import * as executor from '@/wailsjs/go/execute/CommandExecutor'
import * as runtime from '@/wailsjs/runtime/runtime'
import AsyncLock from 'async-lock'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toast-notification'
import type { Command } from './types'
import TaskStatus from './TaskStatus.vue'

defineExpose({
  show: async (
    isParallel_: boolean,
    cmds: Array<Omit<(typeof commands.value)[0], 'prodId' | 'status' | 'result'>>
  ) => {
    show.value = true
    isParallel = isParallel_

    commands.value = cmds.map(vals => ({ ...vals, status: 'pending' }))
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

const commands = ref<Array<Command>>([])

runtime.EventsOn('execute:exited', async (id: string, result: NonNullable<Command['result']>) => {
  const command = commands.value.find(c => c.procId === id)!
  command.result = result

  if (result.aborted) {
    command.status = 'aborted'
  } else if (![0, ...command.allowRtCodes].includes(result.exitCode)) {
    command.status = 'failed'
  } else if (result.lapse < command.minExeTime) {
    command.status = 'speeded'
  } else {
    command.status = 'completed'
  }

  dispatchCommand().then(() => {
    if (commands.value.every(c => c.status === 'completed')) {
      emit('completed')
      $toast.success(t('toasts.finished'), { position: 'bottom-right' })
    } else if (commands.value.every(c => !c.status.includes('ing'))) {
      $toast.info(t('toasts.finished'), { position: 'bottom-right' })
    }
  })
})

async function dispatchCommand() {
  lock.acquire('executor', async () => {
    const pendings = commands.value
      .filter(c => c.status === 'pending')
      .slice(0, isParallel ? undefined : 1)

    for (const command of pendings) {
      if (
        !command.incompatibles.every(id =>
          commands.value.filter(c => c.status === 'running').every(c => c.id != id)
        )
      ) {
        continue
      }

      await executor
        .Run(command.program, command.options)
        .then(processId => {
          command.status = 'running'
          command.procId = processId
        })
        .catch(error => {
          command.status = 'broken'
          command.result = {
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

function handleAbort(command: Command) {
  return lock
    .acquire('executor', () => {
      if (command.status == 'pending' || command.status == 'running') {
        command.status =
          command.procId == undefined || command.procId == '' ? 'aborted' : 'aborting'
      }
    })
    .then(() => {
      if (command.status != 'aborting') {
        return
      }

      // `aborted` status will be updated at `execute:exited` event handler
      executor.Abort(command.procId!).catch(error => {
        if (error.includes('process does not exist')) {
          $toast.warning(t('toasts.cancelCompletedFailed', { name: command.name }))
          return
        }

        error
          .toString()
          .split('\n')
          .forEach((err: string) => {
            if (err.includes('abort failed')) {
              $toast.warning(t('toasts.cancelFailed', { name: command.name }))
            } else {
              $toast.error(`[${command.name}] ${err}`)
            }
          })

        command.status = 'broken'
        command.result = {
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
      <div class="w-[65vw] max-w-[550px] max-h-full p-4">
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
                commands.some(cmd => ['pending', 'running', 'aborting'].includes(cmd.status))
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="max-h-[70vh] overflow-y-auto py-2 px-4">
            <template v-for="(command, i) in commands" :key="i">
              <TaskStatus :cmd="command" @abort="handleAbort(command)"></TaskStatus>
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
