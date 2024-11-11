<script setup lang="ts">
import { ref } from 'vue'
import CrossIcon from '../icons/CrossIcon.vue'
import * as executor from '@/wailsjs/go/execute/CommandExecutor'
import * as runtime from '@/wailsjs/runtime/runtime'

defineExpose({
  show: async (
    isParallel_: boolean,
    cmds: Array<Omit<(typeof commands.value)[0], 'id' | 'status'>>
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

let isParallel: boolean = false
const show = ref(false)
const commands = ref<
  Array<{
    id?: string
    name: string
    status: 'pending' | 'running' | 'finished' | 'failed' | 'aborted'
    program: string
    options: Array<string>
    minExeTime: number
    allowRtCodes: Array<number>
  }>
>([])

runtime.EventsOn(
  'execute:exited',
  (result: { id: string; lapse: number; exitCode: number; stdout: string; stderr: string }) => {
    commands.value.find(c => c.id === result.id)!.status = 'finished'
    dispatchCommand()
  }
)

function dispatchCommand() {
  commands.value.slice(0, isParallel ? undefined : 1).forEach((command, i) => {
    executor.Run(command.program, command.options).then(id => {
      commands.value[i] = {
        ...commands.value[i],
        id: id,
        status: 'running'
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
      <div class="w-[60vw] max-w-[550px] max-h-full p-4">
        <!-- Modal content -->
        <div class="bg-white rounded shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between px-3 py-1.5 border-b rounded-t bg-white">
            <h3 class="font-semibold">
              {{ '執行狀態' }}
            </h3>
            <button
              type="button"
              class="inline-flex justify-center items-center h-8 w-8 ms-auto text-sm text-gray-400 hover:text-gray-900 bg-transparent hover:bg-gray-200 rounded-lg"
              @click="
                () => {
                  show = false
                }
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="max-h-[70vh] overflow-y-auto py-2 px-4">
            <template v-for="(command, i) in commands" :key="i">
              <div class="flex flex-wrap min-h-8 border-t last:border-b border-kashmir-blue-100">
                <div class="content-center w-2/5 pe-1 truncate">{{ command.name }}</div>
                <div class="content-center w-3/5 ps-1 line-clamp-2">等待中</div>
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

label:has(+ input:required, + select:required):after {
  content: ' *';
  color: red;
}
</style>
