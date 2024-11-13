<script setup lang="ts">
import { computed, ref } from 'vue'
import CrossIcon from '@/components/icons/CrossIcon.vue'
import * as executor from '@/wailsjs/go/execute/CommandExecutor'
import * as runtime from '@/wailsjs/runtime/runtime'

defineExpose({
  show: async (
    isParallel_: boolean,
    cmds: Array<Omit<(typeof commands.value)[0], 'prodId' | 'status' | 'result'>>
  ) => {
    show.value = true
    isParallel = isParallel_

    commands.value = cmds.map(vals => ({ ...vals, status: 'pending' }))
    await dispatchCommand()
  },
  hide: () => {
    show.value = false
  }
})

const emit = defineEmits<{ completed: [] }>()

let isParallel: boolean = false

const show = ref(false)

const commands = ref<
  Array<{
    id: string
    procId?: string
    name: string
    status:
      | 'pending'
      | 'running'
      | 'aborting'
      | 'completed'
      | 'failed'
      | 'aborted'
      | 'speeded'
      | 'broken'
    program: string
    options: Array<string>
    minExeTime: number
    allowRtCodes: Array<number>
    incompatibles: Array<string>
    result?: { lapse: number; exitCode: number; stdout: string; stderr: string }
  }>
>([])

const commandQueue = computed(() =>
  commands.value.filter(cmd => cmd.status === 'pending').slice(0, isParallel ? undefined : 1)
)

runtime.EventsOn(
  'execute:exited',
  async (result: {
    id: string
    lapse: number
    exitCode: number
    stdout: string
    stderr: string
  }) => {
    const command = commands.value.find(c => c.procId === result.id)!
    command.result = result

    if (![0, ...command.allowRtCodes].includes(result.exitCode)) {
      command.status = 'failed'
    } else if (result.lapse < command.minExeTime) {
      command.status = 'speeded'
    } else {
      command.status = 'completed'
    }

    await dispatchCommand()
    if (commands.value.every(cmd => cmd.status === 'completed')) {
      emit('completed')
    }
  }
)

async function dispatchCommand() {
  for (const cmd of commandQueue.value) {
    if (
      !cmd.incompatibles.every(id =>
        commands.value.filter(c => c.status === 'running').every(c => c.id != id)
      )
    ) {
      return
    }

    try {
      const id = await executor.Run(cmd.program, cmd.options)
      cmd.procId = id
      cmd.status = 'running'
    } catch {
      cmd.status = 'broken'
      cmd.result = {
        lapse: -1,
        exitCode: -1,
        stdout: '',
        stderr: ''
      }
    }
  }
}

function handleAbort(command: (typeof commands.value)[0]) {
  if (command.procId !== undefined && command.procId !== '') {
    command.status = 'aborting'
    executor
      .Abort(command.procId)
      .then(() => {
        command.status = 'aborted'
      })
      .catch(() => {
        command.status = 'broken'
        command.result = {
          lapse: -1,
          exitCode: -1,
          stdout: '',
          stderr: ''
        }
      })
  } else {
    command.status = 'aborted'
  }
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
              {{ '執行狀態' }}
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
              <div class="flex min-h-9 border-t last:border-b border-kashmir-blue-100">
                <div class="content-center w-2/6 pe-1 text-xs truncate">
                  {{ command.name }}
                </div>

                <div class="flex items-center w-4/6 ps-1 py-1">
                  <template v-if="command.status == 'pending'">
                    <span class="mx-1 px-1.5 bg-gray-300 rounded">等待中</span>

                    <button
                      class="ms-auto mx-1 px-1.5 text-sm bg-kashmir-blue-100 rounded"
                      @click="() => handleAbort(command)"
                    >
                      取消
                    </button>
                  </template>

                  <template v-else-if="command.status == 'running'">
                    <span class="mx-1 px-1.5 bg-half-baked-500 animate-pulse rounded">執行中</span>

                    <button
                      class="ms-auto mx-1 px-1.5 text-sm bg-kashmir-blue-100 rounded"
                      @click="() => handleAbort(command)"
                    >
                      取消
                    </button>
                  </template>

                  <template v-else-if="command.status == 'aborting'">
                    <span class="mx-1 px-1.5 bg-yellow-400 animate-pulse rounded">取消中</span>
                  </template>

                  <template v-else-if="command.status == 'aborted'">
                    <span class="mx-1 px-1.5 bg-gray-400 text-white rounded">已取消</span>
                  </template>

                  <template v-else-if="command.status == 'speeded' || command.status == 'failed'">
                    <div class="shrink-0 w-[4.1rem]">
                      <span class="mx-1 px-1.5 bg-red-300 rounded">失敗</span>
                    </div>

                    <div class="text-sm break-all line-clamp-2">
                      <template v-if="command.status == 'failed'">
                        狀態碼：{{ command.result?.exitCode }}
                      </template>
                      <template v-else>
                        執行時間過快（{{ Math.round(command.result?.lapse ?? -1) }}秒）
                      </template>
                    </div>
                  </template>

                  <template v-else-if="command.status == 'broken'">
                    <div class="shrink-0 w-[4.1rem]">
                      <span class="mx-1 px-1.5 bg-red-700 text-white rounded">錯誤</span>
                    </div>

                    <div class="text-sm break-all line-clamp-2">程式出錯，未能執行</div>
                  </template>

                  <template v-else>
                    <span class="mx-1 px-1.5 bg-apple-green-600 rounded">完成</span>

                    <div class="text-xs text-gray-400 break-all line-clamp-2">
                      執行時間：{{ Math.round(command.result?.lapse ?? -1) }}秒
                    </div>
                  </template>
                </div>
              </div>
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
